import Link from 'next/link'
import Head from 'next/head'
import axios from 'axios'

const fetchData = async () => await axios.get('http://127.0.0.1:8000/episodes/api/episode').then(
  res => ({
    error: false,
    episodes: res.data,
  })).catch(() => ({
    error: true,
    episodes: null,
  }))

const Episodes = ({episodes, error}) => {
  return (
    <>
      <Head>
        <title>CRDB | Episodes</title>
      </Head>
      <div class = "content">
        <ul>
          {episodes.results.map((ep,key) => (
            <li key="ep.title">
              EP {ep.num} 
              <Link href="/episodes/[id]" as={`/episodes/${ep.id}`}>
                <a> {ep.title}</a>
              </Link>
              
              {ep.is_live === true && <span class="tag is-light">Live</span>}
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

export default Episodes