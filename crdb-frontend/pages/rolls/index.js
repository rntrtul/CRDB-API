import Link from 'next/link'
import Head from 'next/head'
import React from 'react'
import axios from 'axios'
import Layout from '../../components/layout'

const fetchData = async () => await axios.get('http://127.0.0.1:8000/rolls/api/roll').then(
  res => ({
    error: false,
    rolls: res.data,
  })).catch(() => ({
    error: true,
    rolls: null,
  }))
function timeFormat(secs) {
    return new Date(secs * 1000).toISOString().substr(12, 7)
  }

const RollTable = ({rolls, error}) => {
  return (
    <>
      <Head>
        <title>CRDB | Rolls</title>
      </Head>
      <table className = "table is-bordered is-striped">
        <thead>
          <tr>
            <th>Time Stamp</th>
            <th>Character</th>
            <th>Roll Type</th>
            <th>Final Value</th>
            <th>Natural Value</th>
            <th>Notes</th>
            <th>Damage</th>
            <th>Kills</th>
          </tr>
        </thead>
        <tbody>     
          {rolls.results.map((roll,key) => (
            <tr>
              <td>{timeFormat(roll.time_stamp)}</td>
              <td>{roll.character}</td>
              <td>{roll.roll_type}</td>
              <td>{roll.final_value}</td>
              <td>{roll.natural_value}</td>
              <td>{roll.notes}</td>
              <td>{roll.damage}</td>
              <td>{roll.kill_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}

export const getServerSideProps = async () => {
  const data = await fetchData();
  return {
    props: data,
  };
}

export default RollTable