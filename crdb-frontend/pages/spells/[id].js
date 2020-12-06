import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import {get_yt_link, timeFormat} from '../../components/helpers'

function SpellDetail({spell}) { 
  let above_cast = 0
  spell.casts.map((casting) => casting.cast_level > spell.level && above_cast++ )
  return (
    <div className = "content">
      <Head><title>CRDB | {spell.name}</title></Head>
      <p className="title">{spell.name}</p>
      <p className="subtitle">
        {spell.cantrip === true && <span>Cantrip</span>}
        {spell.cantrip === false && <span>Level: {spell.level}</span>}
      </p>
      <p>Total casts: {spell.casts.length}</p>
      <p>Times cast above level: {above_cast} </p>
      <p className = "heading">Top Casters:</p>
      <ol>
        {spell.top_users.map((rank) =>
          <li>{rank[0]} ({rank[1]})</li>
        )}
      </ol>
      <table className="table is-striped">
        <thead>
          <tr>
            <th>Time Stamp</th>
            <th>Character</th>
            <th>Cast Level</th>
            <th>Episode</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {spell.casts.map((cast) => 
            <tr>
              <td>
                <a href={get_yt_link(cast.timestamp, cast.notes, cast.episode.vod_links)}>
                  {timeFormat(cast.timestamp)}
                </a>
              </td>
              <td>
                <Link href="/characters/[id]" as={`/characters/${cast.character.id}`}>
                  <a>{cast.character.name}</a>
                </Link>
              </td>
              <td>{cast.cast_level}</td>
              <td>
                <Link href = "/episodes/[id]" as = {`/episodes/${cast.episode.id}`}>
                  <a>{cast.episode.title} </a>
                </Link>
                ({cast.episode.num})
              </td>
              <td>{cast.notes}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export async function getStaticPaths() {
  const data = (await axios.get('https://critroledb-api.herokuapp.com/spells/api/spell')).data
  const paths = data.results.map((spell) => ({
    params: {id: spell.id.toString()},
  }))
  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  const spell = (await axios.get(`https://critroledb-api.herokuapp.com/spells/api/spell/${params.id}`)).data
  return { props: { spell},revalidate: 3 }
} 

export default SpellDetail