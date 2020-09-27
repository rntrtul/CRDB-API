import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import Table, { defaultSortComparator } from 'mineral-ui/Table'
import { ThemeProvider } from 'mineral-ui/themes'
import { get_yt_link, timeFormat} from '../../components/helpers'
import ReactFrappeChart from "react-frappe-charts"

function EpisodeDetail({episode, roll_type}) { 
  const rolls_columns = [
    { content: 'Time Stamp'   , key: 'time_stamp', primary: true},
    { content: 'Character'    , key: 'character'},
    { content: 'Roll Type'    , key: 'roll_type'},
    { content: 'Natural Value', key: 'natural_value'},
    { content: 'Final Value'  , key: 'final_value'},
    { content: 'Notes'        , key: 'notes'},
    { content: 'Damage'       , key: 'damage'},
    { content: 'Kills'        , key: 'kill_count'}
  ]

  const casts_columns = [
    {content: 'Time Stamp', key: 'time_stamp', primary: true},
    {content: 'Spell', key: 'spell'},
    {content: 'Character', key: 'character'},
    {content: 'Cast Lvl', key: 'cast_level'},
    {content: 'notes', key: 'notes'},
  ]
  
  const rolls_display = episode.rolls.map((roll) => {
    let yt_link = get_yt_link(roll.time_stamp, roll.notes, episode.vod_links)
    return {
      "time_stamp": <a href={yt_link}>{timeFormat(roll.time_stamp)}</a>,
      "character": <Link href = "/characters/[id]" as={`/characters/${roll.character.id}`}><a>{roll.character.name}</a></Link>,
      "roll_type": <Link href="/rolls/types/[id]" as={`/rolls/types/${roll.roll_type.id}`}><a>{roll.roll_type.name}</a></Link>,
      "natural_value": roll.natural_value,
      "final_value": roll.final_value,
      "notes": roll.notes,
      "damage": roll.damage,
      "kill_count": roll.kill_count,
    }
  })

  const casts_display = episode.casts.map((cast) => {
    let yt_link = get_yt_link(cast.timestamp, cast.notes, episode.vod_links)
    return {
      "time_stamp": <a href={yt_link}>{timeFormat(cast.timestamp)}</a>,
      "spell": <Link href = "/spells/[id]" as = {`/spells/${cast.spell.id}`}><a>{cast.spell.name}</a></Link>,
      "character": <Link href = "/characters/[id]" as={`/characters/${cast.character.id}`}><a>{cast.character.name}</a></Link>,
      'cast_level': cast.cast_level, 
      "notes": cast.notes,
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
          {episode.attendance.map((player) => <li key = {player.player.full_name}> {player.player.full_name} </li> )}
        </ul>
        
        <h4>Characters in</h4>
        <ul>
          {episode.apperances.map((app) => <li key={app.character.name}> {app.character.name} </li> )}
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

        <h3>Spells Cast ({episode.casts.length})</h3>
        <ThemeProvider id = "table">
          <Table
            striped
            columns={casts_columns}
            data={casts_display}
            sortable
            rowKey='time_stamp'
            title="Episode Spell Casts"
            hideTitle />
        </ThemeProvider>

        <h3>Rolls ({episode.rolls.length})</h3>

        <ThemeProvider id = "table">
          <Table
            striped
            columns={rolls_columns}
            data={rolls_display}
            sortable
            rowKey='time_stamp'
            title="Episode Rolls"
            hideTitle />
        </ThemeProvider>
      
      </div>
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
  return { props: { episode } }
} 

export default EpisodeDetail