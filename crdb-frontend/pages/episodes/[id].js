import axios from 'axios'
import Head from 'next/head'

const fetchData = async () => await axios.get('http://127.0.0.1:8000/episodes/api/episode/' + useRouter.query).then(
  res => ({
    error: false,
    detail: res.data,
  })).catch(() => ({
    detail: null,
    error: true,
  }))

function timeFormat(secs) {
  return new Date(secs * 1000).toISOString().substr(12, 7)
}
  
function EpisodeDetail({episode}) { 
  return (
    <div>
      <Head>
        <title>{episode.title}</title>
      </Head>
      <h1>{episode.title}</h1>
      <h2>{episode.num}</h2>
      <h4>{episode.description}</h4>
      <p>Length: {timeFormat(episode.length)}</p>
      <p>Break length: {timeFormat(episode.second_half_start - episode.first_half_end)}</p>
      <p>First half start: {timeFormat(episode.first_half_start)}</p>
      <p>First half end: {timeFormat(episode.first_half_end)}</p>
      <p>Second half start: {timeFormat(episode.second_half_start)}</p>
      <p>Second half end: {timeFormat(episode.second_half_end)}</p>

      <h3>Combat Encounters</h3>
      <ul>
        {episode.combat_encounters.map((encounter) => 
        <li>
          {encounter.name}, starts at {timeFormat(encounter.start)}, end at {timeFormat(encounter.end)}, rounds: {encounter.rounds}
        </li>
        )}
      </ul>
      <h3>Players in</h3>
      <ul>
        {episode.attendance.map((attendance) => 
          <li>
            {attendance.player.full_name} {attendance.attendance_type.name != 'normal' && attendance.attendance_type.name}
          </li>
        )}
      </ul>
    </div>
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