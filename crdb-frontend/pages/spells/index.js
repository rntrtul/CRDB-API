import Link from 'next/link'
import Head from 'next/head'
import axios from 'axios'

// eventually change charactype from 1 to pc (use name not int id)
// change to using api (witch will call fetcher
const fetchData = async () => await axios.get('http://127.0.0.1:8000/spells/api/spell').then(
  res => ({
    error: false,
    spells: res.data.results,
  })).catch(() => ({
    error: true,
    spells: null,
  }))

const Spells = ({spells, error}) => {
  return (
    <>
      <Head>
        <title>CRDB | Spells</title>
      </Head>
      <div class = "content">
        <ul>
          {spells.map((spell,key) => (
            <li key="spell.name"> 
              <Link href="/spells/[id]" as={`/spells/${spell.id}`}>
                <a>{spell.name}</a>
              </Link>
              <span> ({spell.cast_count})</span>
            </li>
          ))}
        </ul>
      </div>
    </> 
  )
}

export const getServerSideProps = async () => {
  const data = (await fetchData());
  return {
    props: data,
  };
}

export default Spells