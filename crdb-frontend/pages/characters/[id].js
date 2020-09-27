import axios from 'axios'
import Link from 'next/link'
import Head from 'next/head'
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs'
import StatSheet from '../../components/statsheet'
import ReactFrappeChart from "react-frappe-charts"

function CharacterDetail({character}) { 
  let normal_rolls = character.roll_counts.total - character.roll_counts.advantages - character.roll_counts.disadvantages
  let roll_data = [character.roll_counts.disadvantages, character.roll_counts.advantages, normal_rolls]
  let roll_colours = ['red', 'blue', 'light-blue']
  let roll_labels = ["Disadvantage", "Advantage", "Normal"]

  let insert_type = (num, name, colour, colour_arr, data_arr, label_arr) => {
    data_arr.splice(-1,0,num)
    data_arr[-1] = roll_data[-1] - roll_data[-2]
    label_arr.splice(-1,0,name)
    colour_arr.splice(-1,0,colour)
  }

  if (character.roll_counts.luck !== 0) insert_type(character.roll_counts.luck, "Luck", "green", roll_colours, roll_data, roll_labels)
  if (character.roll_counts.fate !== 0) insert_type(character.roll_counts.fate, "Fate", "orange", roll_colours, roll_data, roll_labels)
  if (character.roll_counts.decahedron !== 0) insert_type(character.roll_counts.decahedron, "Fragment of Possibility", "purple", roll_colours, roll_data, roll_labels)
  
  return (
    <div className = "content">
      <Head><title>CRDB | {character.name}</title></Head>
      <h1 className= "title is-2">{character.full_name}</h1>
      <p>Player: {character.player.full_name}</p>
      <p>Race: {character.race.name}</p>
      <p>Character Type: {character.char_type.name}</p>

      <Tabs selectedTabClassName = "is-active">
        <TabList className = "tabs is-centered">
          <ul>
            <Tab><li><a>Stats</a></li></Tab>
            <Tab><li><a>Stat Sheet</a></li></Tab>
            <Tab><li><a>Rolls</a></li></Tab>
            <Tab><li><a>Apperances</a></li></Tab>
            <Tab><li><a>Spells</a></li></Tab>
          </ul>
        </TabList>

        <TabPanel>
        <>
          <div className="tile is-ancestor">
            <div className = "tile is-parent">
              <div className = "tile is-child box">
                <div className = "level is-mobile">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className="heading">Damage Dealt</p>
                      <p className="title">{character.damage_total.final_value__sum}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className = "tile is-parent">
              <div className = "tile is-child box">
                <div className = "level is-mobile">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className="heading">Natural 1's</p>
                      <p className="title">{character.nat_ones}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className = "tile is-parent">
              <div className = "tile is-child box">
                <div className = "level is-mobile">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className="heading">Natural 20's</p>
                      <p className="title">{character.nat_twenty}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className = "tile is-parent">
              <div className = "tile is-child box">
                <div className = "level is-mobile">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className="heading">HDYWTDT</p>
                      <p className="title">{character.hdywt_count}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className = "tile is-parent">
              <div className = "tile is-child box">
                <div className = "level is-mobile">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className="heading">Kills</p>
                      <p className="title">{character.kill_count.kill_count__sum}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <ReactFrappeChart
            type="percentage"
            title={"Rolls (" + character.roll_counts.total + " total)"}
            colors={roll_colours}
            barOptions={{depth:0}}
            
            data={{
              labels: roll_labels,
              datasets: [{ values: roll_data}], 
            }}          
          />

          <div className="tile is-ancestor">
            <div className = "tile is-parent">  
              <div className = "tile is-child">
                <ReactFrappeChart
                  type="bar"
                  title="Top Roll Types"
                  colors={['blue']}
                  axisOptions={{ xAxisMode: "tick"}}
                  valuesOverPoints={true}
                  tooltipOptions={{
                    formatTooltipY: d=> d > 1 ? d + " rolls" : d + " roll"
                  }}
                  data={{
                    labels: character.top_roll_types.map((type) => type[0]),
                    datasets: [{ values: character.top_roll_types.map((type) => type[1])}], 
                  }}
                />
              </div>      
            </div>
            <div className = "tile is-parent">
              <div className = "tile is-child no_x_axis">
              <ReactFrappeChart
                type="bar"
                title="Rolls Per Episode"
                colors={['green']}
                axisOptions={{ xAxisMode: "tick"}}
                tooltipOptions={{
                  formatTooltipX: d => "EP " + d,
                  formatTooltipY: d=> d > 1 ? d + " rolls" : d + " roll"
                }}
                data={{
                  labels: [...Array(character.campaign.length).keys()].map(x => x + 1),
                  datasets: [{ values: character.ep_totals.rolls}], 
                  yMarkers: [{
                    label: "Avg.",
                    value: character.ep_totals.rolls.reduce((a,b) => a + b) / character.apperances.length,
                    options: { labelPos: 'left' }
                  }]
                }}
              />
              </div>
            </div>
          </div>

          {character.top_spells.total_count > 0 &&
            <div className = "tile is-ancestor">
              <div className = "tile is-parent">
                <div className = "tile is-child">
                  <ReactFrappeChart
                    type="bar"
                    title={"Top Spells Cast (" + character.top_spells.total_count + " total)"}
                    colors={['light-blue']}
                    axisOptions={{ xAxisMode: "tick"}}
                    valuesOverPoints={true}
                    tooltipOptions={{
                      formatTooltipY: d=> d > 1 ? d + " casts" : d + " cast"
                    }}
                    data={{
                      labels: character.top_spells.list.map((spell) => spell[0]),
                      datasets: [{ values: character.top_spells.list.map((spell) => spell[1])}], 
                    }}
                  />
                </div>
              </div>
              <div className = "tile is-parent">
                <div className = "tile is-child no_x_axis">
                  <ReactFrappeChart
                    type="bar"
                    title={"Cast Per Episode"}
                    colors={['light-green']}
                    axisOptions={{ xAxisMode: "tick"}}
                    tooltipOptions={{
                      formatTooltipX: d=> "EP "  + d,
                      formatTooltipY: d=> d > 1 ? d + " casts" : d + " cast"
                    }}
                    data={{
                      labels: [...Array(character.campaign.length).keys()].map(x => x + 1),
                      datasets: [{ values: character.ep_totals.casts}],
                      yMarkers: [{
                        label: "Avg.",
                        value: character.ep_totals.casts.reduce((a,b) => a + b) / character.apperances.length,
                        options: { labelPos: 'left' }
                      }],
                    }}
                  />
                </div>
              </div>
              
            </div>          
          }
          <div className = "no_x_axis">
            <ReactFrappeChart
              type="bar"
              title={"Damage Dealt Per Ep"}
              colors={['blue']}
              axisOptions={{ xAxisMode: "tick"}}
              tooltipOptions={{
                formatTooltipX: d=> "EP "  + d,
                formatTooltipY: d=> d + " dmg"
              }}
              data={{
                labels: [...Array(character.campaign.length).keys()].map(x => x + 1),
                datasets: [{ values: character.ep_totals.dmg_dealt}],
                yMarkers: [{
                  label: "Avg.",
                  value: character.ep_totals.dmg_dealt.reduce((a,b) => a + b) / character.apperances.length,
                  options: { labelPos: 'left' }
                  }],
                }}
              />
            </div>      
        </>
        </TabPanel>
        <TabPanel>
            <StatSheet data ={character.sheets}></StatSheet>
        </TabPanel>
        <TabPanel><p>Show character roll table</p></TabPanel>
        <TabPanel>
          <h4>Appears in ({character.apperances.length}):</h4>
          <ul>
            {character.apperances.map((apperance) => 
            <li key = {apperance.episode}><Link href={`/episodes/${apperance.episode}`}><a>{apperance.episode_title}</a></Link></li>
            )}
          </ul>
        </TabPanel>
        <TabPanel><p>Add table of all spells cast</p></TabPanel>
      </Tabs>
    </div>
  )
}

export async function getStaticPaths() {
  const data = (await axios.get('http://127.0.0.1:8000/characters/api/character')).data
  const paths = data.results.map((character) => ({
    params: {id: character.id.toString()},
  }))
  return {paths, fallback: false}
}

export async function getStaticProps({params}){
  const character = (await axios.get(`http://127.0.0.1:8000/characters/api/character/${params.id}`)).data
  return { props: {character},revalidate: 120 }
} 

export default CharacterDetail