import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import ReactFrappeChart from "react-frappe-charts"
import {timeFormat, get_yt_link} from '../../../components/helpers'

function WeaponDetail({weapon }) { 
  return (
    <div className = "content">
      <h1>{weapon.name}</h1>
      <p className="subtitle">
        { weapon.damages.map((dt, i) => 
          <span>{dt.die_num}d{dt.die.sides} {dt.modifier > 0 && <> + {dt.modifier}</>} {dt.damage_type > 0 &&dt.damage_type.name}{i < weapon.damages.length - 1 && <b> + </b>}</span>
        )}
      </p>
      <p>This is not damage but to attack (next roll should be damage)</p>
      <p>Total Damage Done With: {weapon.dmg_total[0].final_total}</p>
      <p>Total Damage Contributated: {weapon.dmg_total[1].nat_total}</p>
      <p>Total uses: {weapon.uses.length}</p>
      
      <table className='table is-striped is-fullwidth'>
        <thead>
          <tr>
            <td>Episode</td>
            <td>Time Stamp</td>
            <td>Character</td>   
            <td>Roll Type</td>             
            <td>Natural Value</td>
            <td>Final Value</td>
            <td>Notes</td>
            <td>Damage</td>  
          </tr>
        </thead>
        <tbody>
          {weapon.uses.map((use) =>
            <tr>
              <td>
                <Link href="/episodes/[id]" as = {`/episodes/${use.roll.ep.id}`}>
                  <a>C{use.roll.ep.campaign_num}E{use.roll.ep.num}</a>
                </Link>
              </td>
              <td>
                <a href = {get_yt_link(use.roll.time_stamp, use.roll.notes, use.roll.ep.vod_links)}>{timeFormat(use.roll.time_stamp)}</a>
              </td>
              <td>{use.roll.character.name}</td>
              <td>{use.roll.roll_type.name}</td>
              <td>{use.roll.natural_value}</td>
              <td>{use.roll.final_value}</td>
              <td>{use.roll.notes}</td>
              <td>{use.roll.damage}</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}

export async function getStaticPaths() {
  const data = (await axios.get('https://critroledb-api.herokuapp.com/items/api/weapon')).data
  const paths = data.results.map((weapon) => ({
    params: {id: weapon.id.toString()},
  }))
  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  const weapon = (await axios.get(`https://critroledb-api.herokuapp.com/items/api/weapon/${params.id}`)).data
  return { props: {weapon},revalidate: 600 }
} 

export default WeaponDetail