import Link from 'next/link'
import Head from 'next/head'
import axios from 'axios'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';

const Items = (items) => {
  const potions = items.potions.data.results
  const weapons = items.weapons.data.results
  return (
    <>
    <Head>
      <title>CRDB | Items</title>
    </Head>
    <div class = "content">
      <Tabs selectedTabClassName="is-active">
        <TabList>
          <div class = "tabs is-centered">
            <ul>
              <Tab><li><a>Weapons</a></li></Tab>
              <Tab><li><a>Potions</a></li></Tab>
            </ul>
          </div>
        </TabList>

        <TabPanel>
          <ul>
            {weapons.map((weapon, key) => 
              <li key = {weapon.id}>
                <Link href = "items/weapons/[id]" as ={`/items/weapons/${weapon.id}`}><a>{weapon.name}</a></Link>
              </li>
            )}
          </ul> 
        </TabPanel>

        <TabPanel>
          <ul>
            {potions.map((potion, key) => 
              <li key = {potion.id}>
                <Link href="/items/potions/[id]" as ={`/items/potions/${potion.id}`}><a>{potion.name}</a></Link>
              </li>
            )}
          </ul>
        </TabPanel>
      </Tabs>        
    </div>
    </> 
  )
}


const fetchData = async (url) => await axios.get(url).then(
  res => ({
    error: false,
    data: res.data,
  })).catch(() => ({
    error: true,
    data: null,
  }))

export async function getServerSideProps(){
  const potions = await fetchData('http://127.0.0.1:8000/items/api/potion')
  const weapons = await fetchData('http://127.0.0.1:8000/items/api/weapon')
  const items = {
    'potions': potions,
    'weapons': weapons,
  }
  return {props: items};  
}

export default Items