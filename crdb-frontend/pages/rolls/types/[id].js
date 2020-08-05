import axios from 'axios'

function RollType ({roll_type}){
  return (
    <div class="content">
      <h1>{roll_type.name}</h1>
      <h3>Count: {roll_type.count}</h3>
    </div>
  )
}

export async function getStaticPaths() {
  const data = (await axios.get('http://127.0.0.1:8000/rolls/api/rolltype')).data
  const paths = data.results.map((type) => ({
    params: {id: type.id.toString()},
  }))

  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  console.log(params)
  const roll_type = (await axios.get(`http://127.0.0.1:8000/rolls/api/rolltype/${params.id}`)).data
  return { props: {roll_type } }
} 

export default RollType