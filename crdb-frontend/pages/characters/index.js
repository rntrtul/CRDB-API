import Link from 'next/link'
import Head from 'next/head'
import axios from 'axios'

// eventually change charactype from 1 to pc (use name not int id)
const fetchData = async () => await axios.get('https://critroledb-api.herokuapp.com/characters/api/charactertype/1').then(
  res => ({
    error: false,
    characters: res.data,
  })).catch(() => ({
    error: true,
    characters: null,
  }))

const Characters = ({characters, error}) => {
  return (
    <>
      <Head>
        <title>CRDB | Characters</title>
      </Head>
      <div class = "tabs">
        <ul>
          <li class ="is-active"><a>PC</a></li>
          <li><a>NPC</a></li>
        </ul>
      </div>
      <div class = "content">
        <ul>
          {characters.characters.sort((a,b) => a.name > b.name).map((char,key) => (
            <li key="char.name"> 
              <Link href="/characters/[id]" as={`/characters/${char.id}`}>
                <a>{char.name}</a>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </> 
  )
}

export const getServerSideProps = async () => {
  const data = await fetchData();
  return {
    props: data,
  };
}

export default Characters