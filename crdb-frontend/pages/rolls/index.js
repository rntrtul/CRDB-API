import Head from 'next/head'
import React from 'react'
import axios from 'axios'
import {timeFormat} from '../../components/helpers'
import { RollTable } from '../../components/rolltable'
import FilterForm from '../../components/filter'
const fetchData = async () => await axios.get('https://critroledb-api.herokuapp.com/rolls/api/roll').then(
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
      <FilterForm/>
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