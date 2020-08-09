import Head from 'next/head'
import React from 'react'
import axios from 'axios'
import {timeFormat} from '../../components/helpers'
import { RollTable } from '../../components/rolltable'

const fetchData = async () => await axios.get('http://127.0.0.1:8000/rolls/api/roll').then(
  res => ({
    error: false,
    rolls: res.data,
  })).catch(() => ({
    error: true,
    rolls: null,
  }))

const Table = ({rolls, error}) => {
  return (
    <>
      <Head>
        <title>CRDB | Rolls</title>
      </Head>
      <RollTable data={rolls.results}/>
    </>
  )
}

export const getServerSideProps = async () => {
  const data = await fetchData();
  return {
    props: data,
  };
}

export default Table