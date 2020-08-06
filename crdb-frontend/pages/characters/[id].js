import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import { Tabs, Tab, Panel } from '@bumaga/tabs' 

function CharacterDetail({character}) { 
  return (

    <div class = "content">
      <Head><title>{character.name}</title></Head>
      <h1>{character.full_name}</h1>
      <p>Player: {character.player.full_name}</p>
      <p>Race: {character.race.name}</p>
      <p>Character Type: {character.char_type.name}</p>

      <Tabs>
        <div class = "tabs is-centered">
          <ul>          
            <li><Tab><a>Stats</a></Tab></li>
            <li><Tab><a>Rolls</a></Tab></li>
            <li><Tab><a>Apperances</a></Tab></li>
            <li><Tab><a>Charts</a></Tab></li>
            <li><Tab><a>Stat Sheet</a></Tab></li>
          </ul>
        </div>

        <Panel><p>Show some stats</p></Panel>
        <Panel><p>Show cahracter rolls</p></Panel>
        <Panel>
          <h4>Appears in ({character.apperances.length}):</h4>
          <ul>
            {character.apperances.sort((a,b) => a.episode.num - b.episode.num).map((apperance) => 
            <li><Link href={`/episodes/${apperance.episode.id}`}><a>{apperance.episode.title}</a></Link></li>
            )}
          </ul>
        </Panel>
        <Panel><p>Show charts about character</p></Panel>
        <Panel>
          <div class ="select">
            <select>
              <option>Level 8</option>
              <option>Level 7</option>
              <option>Level 6</option>
            </select>
            
          </div>
        </Panel>
      </Tabs>
      
    </div>
  )
}

// un depth apperance (backend)
export async function getStaticPaths() {
  const data = (await axios.get('http://127.0.0.1:8000/characters/api/character')).data
  const paths = data.results.map((character) => ({
    params: {id: character.id.toString()},
  }))
  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  const character = (await axios.get(`http://127.0.0.1:8000/characters/api/character/${params.id}`)).data
  //const roll_type = (await axios.get("http://127.0.0.1:8000/rolls/api/rolltype")).data
  return { props: { character},revalidate: 3 }
} 

export default CharacterDetail