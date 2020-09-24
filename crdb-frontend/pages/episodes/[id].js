import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import Table, { defaultSortComparator } from 'mineral-ui/Table'
import { ThemeProvider } from 'mineral-ui/themes'
import { get_yt_link, timeFormat} from '../../components/helpers'
import ReactFrappeChart from "react-frappe-charts"

function EpisodeDetail({episode, roll_type}) { 
  const columns = [
    { content: 'Time Stamp'   , key: 'time_stamp', primary: true},
    { content: 'Character'    , key: 'character'},
    { content: 'Roll Type'    , key: 'roll_type'},
    { content: 'Natural Value', key: 'natural_value'},
    { content: 'Final Value'  , key: 'final_value'},
    { content: 'Notes'        , key: 'notes'},
    { content: 'Damage'       , key: 'damage'},
    { content: 'Kills'        , key: 'kill_count'}
  ]

  const player_display = episode.attendance.sort((a,b) => a.player.full_name > b.player.full_name).map((elemn) => {
    let display = elemn.player.full_name
    if (elemn.attendance_type.name != 'normal'){
      display = display + " (" + elemn.attendance_type.name + ")"
    } 
    return display
  });

  const character_display = episode.apperances.sort((a,b) => a.character.full_name > b.character.full_name).map((elemn) => {
    return elemn.character.full_name
  });
  
  const getCharName = (char_id) => {
    for (let idx in episode.apperances){
      if (episode.apperances[idx].character.id === char_id){
        return episode.apperances[idx].character.name
      }
    }
    return false
  }

  const getRollType = (type_id) => {
    for (let idx in roll_type.results){
      if (roll_type.results[idx].id === type_id){
        return roll_type.results[idx].name
      }
    }
    return false
  }
  
  const rolls_display = episode.rolls.map((roll) => {
    let char_name = getCharName(roll.character_id)
    let type_name = getRollType(roll.roll_type_id)
    let yt_link = get_yt_link(roll.time_stamp, roll.notes, episode.vod_links)
    return {
      "time_stamp": <a href={yt_link}>{timeFormat(roll.time_stamp)}</a>,
      "character": <Link href = "/characters/[id]" as={`/characters/${roll.character_id}`}><a>{char_name}</a></Link>,
      "roll_type": <Link href="/rolls/types/[id]" as={`/rolls/types/${roll.roll_type_id}`}><a>{type_name}</a></Link>,
      "natural_value": roll.natural_value,
      "final_value": roll.final_value,
      "notes": roll.notes,
      "damage": roll.damage,
      "kill_count": roll.kill_count
    }
  })

  return (
    <>
      <Head><title>{episode.title}</title></Head>
      <div class = "content is-medium">
        <h1>{episode.title} (C{episode.campaign.num}E{episode.num}) </h1>
        <h4>{episode.air_date}</h4>
        <p class = "is-medium">{episode.description}</p>
        <p>Length: {timeFormat(episode.length)}</p>
      </div>

      <div class = "content">

        <h5>Times:</h5>
        <ReactFrappeChart
          type="percentage"
          title="Time Breakdown"
          colors={['dark-grey', 'blue', 'dark-grey', 'blue', 'dark-grey']}
          barOptions={{depth:0}}
          tooltipOptions={{
            formatTooltipX: d => "et",
            formatTooltipY: d => " ads"
          }}
          data={{
            labels: ["Anouncments", "First Half", "Break", "Second Half", "End"],
            datasets: [{ values:
              [episode.first_half_start,
               episode.first_half_end - episode.first_half_start,
               episode.second_half_start - episode.first_half_end,
               episode.second_half_end - episode.second_half_start,
               episode.length - episode.second_half_end]
            }], 
          }}
          
        />
        
        <p>Break length: {timeFormat(episode.second_half_start - episode.first_half_end)}</p>
        <p>First half start: {timeFormat(episode.first_half_start)}</p>
        <p>First half end: {timeFormat(episode.first_half_end)}</p>
        <p>Second half start: {timeFormat(episode.second_half_start)}</p>
        <p>Second half end: {timeFormat(episode.second_half_end)}</p>

        <h4>Players in</h4>
        <ul>
          {player_display.map((player_name) => <li key = {player_name}> {player_name} </li> )}
        </ul>
        
        <h4>Characters in</h4>
        <ul>
          {character_display.map((char_name) => <li key={char_name}> {char_name} </li> )}
        </ul>

        {episode.level_ups.length > 0 &&
          <>
            <h4>Level ups this episode:</h4>
            <ul>
              {episode.level_ups.map((level_up) => 
                <li key={level_up.char_id}> {level_up.char_name} leveled up to {level_up.level} </li> )}
            </ul>
          </>
        }

        {episode.combat_encounters.length > 0 &&
          <>
            <h4>Combat Encounters</h4>
            <ul>
              {episode.combat_encounters.map((encounter) => 
              <li>
                {encounter.name}, starts at {timeFormat(encounter.start)}, end at {timeFormat(encounter.end)}, rounds: {encounter.rounds}
              </li> )}
            </ul>
          </>
        }

        <h3>All Rolls ({Object.keys(episode.rolls).length})</h3>
      </div>
     
      <ThemeProvider id = "table">
        <Table
          striped
          columns={columns}
          data={rolls_display}
          sortable
          rowKey='time_stamp'
          title="Episode Rolls"
          hideTitle />
      </ThemeProvider>
    </>
  )
}

export async function getStaticPaths() {
  const data = (await axios.get('http://127.0.0.1:8000/episodes/api/episode')).data
  const paths = data.results.map((episode) => ({
    params: {id: episode.id.toString()},
  }))

  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  const episode = (await axios.get(`http://127.0.0.1:8000/episodes/api/episode/${params.id}`)).data
  const roll_type = (await axios.get("http://127.0.0.1:8000/rolls/api/rolltype")).data
  return { props: { episode, roll_type } }
} 

export default EpisodeDetail