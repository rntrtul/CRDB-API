import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import ReactFrappeChart from "react-frappe-charts"
import {timeFormat, get_yt_link} from '../../../components/helpers'

function PotionDetail({potion}) { 
  return (
    <div className = "content">
      <h1>{potion.name}</h1>
      <p className="subtitle">{potion.description} (should be description here)</p>
      <h4>All Uses ({potion.uses.length}):</h4>
      <table className='table is-striped is-fullwidth'>
        <thead>
          <tr>
            <td>Episode</td>
            <td>Time Stamp</td>
            <td>By</td>
            <td>To</td>
            <td>Notes</td>            
          </tr>
        </thead>
        <tbody>
          {potion.uses.map((use) =>
            <tr>
              <td>
                <Link href="/episodes/[id]" as = {`/episodes/${use.episode.id}`}>
                  <a>C{use.episode.campaign.num}E{use.episode.num}</a>
                </Link>
              </td>
              <td>
                <a href = {get_yt_link(use.timestamp, use.notes, use.episode.vod_links)}>{timeFormat(use.timestamp)}</a>
              </td>
              <td>
                <Link href = "/characters/[id]" as = {`/characters/${use.by.id}`}><a>{use.by.name}</a></Link>
              </td>
              <td>
                <Link href = "/characters/[id]" as = {`/characters/${use.to.id}`}><a>{use.to.name}</a></Link>  
              </td>
              <td>{use.notes}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export async function getStaticPaths() {
  const data = (await axios.get('https://critroledb-api.herokuapp.com/items/api/potion')).data
  const paths = data.results.map((potion) => ({
    params: {id: potion.id.toString()},
  }))
  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  const potion = (await axios.get(`https://critroledb-api.herokuapp.com/items/api/potion/${params.id}`)).data
  return { props: {potion},revalidate: 600 }
} 

export default PotionDetail