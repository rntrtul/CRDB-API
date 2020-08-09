import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import { Tabs, Tab, Panel } from '@bumaga/tabs' 
import StatSheet from '../../components/statsheet'

function CharacterDetail({character}) { 
  return (

    <div className = "content">
      <Head><title>{character.name}</title></Head>
      <h1>{character.full_name}</h1>
      <p>Player: {character.player.full_name}</p>
      <p>Race: {character.race.name}</p>
      <p>Character Type: {character.char_type.name}</p>

      <Tabs>
        <div className = "tabs is-centered">
          <ul>          
            <li><Tab><a>Stat Sheet</a></Tab></li>
            <li><Tab><a>Rolls</a></Tab></li>
            <li><Tab><a>Apperances</a></Tab></li>
            <li><Tab><a>Charts</a></Tab></li>
            <li><Tab><a>Stats</a></Tab></li>
          </ul>
        </div>

        <Panel>
            <StatSheet data ={character.sheets}></StatSheet>
         
        </Panel>
        <Panel><p>Show cahracter rolls</p></Panel>
        <Panel>
          <h4>Appears in ({character.apperances.length}):</h4>
          <ul>
            {character.apperances.map((apperance) => 
            <li key = {apperance.episode}><Link href={`/episodes/${apperance.episode}`}><a>{apperance.episode_title}</a></Link></li>
            )}
          </ul>
        </Panel>
        <Panel><p>Show charts about character</p></Panel>
        <Panel>
          <>
          <p>Total Rolls: {character.roll_count}</p>
          <p>Total Damage Dealt: {character.damage_total.final_value__sum}</p>
          <p>Total Nat1's: {character.nat_ones}</p>
          <p>Total Nat20's: {character.nat_twenty}</p>
          <p>HDYWTDT: {character.hdywt_count}</p>
          <p>Times had advantage:</p>
          <p>Times had disadvantage:</p>
          <p>Kills: {character.kill_count.kill_count__sum}</p>
          {character.top_spells.length > 0 &&
            <>
              <p>Top 10 spells cast</p>
              <ol>
                {character.top_spells.map((spell) => <li key={spell[0]}>{spell[0]} ({spell[1]})</li>)}
              </ol>
            </>          
          }
          <p>Top 10 Roll types:</p>
          <ol>
            {character.top_roll_types.map((roll_type) => <li key={roll_type[0]}>{roll_type[0]} ({roll_type[1]})</li>)}
          </ol>
          </>
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
  return { props: { character},revalidate: 3 }
} 

export default CharacterDetail