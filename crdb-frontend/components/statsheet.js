import React, { useState } from "react"
import { useFetch } from './fetcher'

const StatSheet = () => {
  const [query, setQuery] = useState('');
  const url = query && `http://127.0.0.1:8000/characters/api/statsheet/1608`
  const {status, data, error} = useFetch(url)

  const sheet = data
  console.log(sheet)

  const handleSubmit = (e) => {
    console.log("Handeling submit")
    console.log(e)
    e.preventDefault();

		const query = e.target.select.value;
		if (query) {
			setQuery(query);
		}
  };  

  return (
    //{character.sheets.map((sheet) => <option key ={sheet.sheet_level}>Level {sheet.sheet_level}</option> )}
    // store ability scores in an array for use maybe, pre process that
    <>
      <form onSubmit={handleSubmit}>
        <div class="field has-addons">
          <div class="control">
            <div className ="select is-fullwidth">
              <select name="select">
                <option value="11">Level 11</option>
              </select>
            </div>
          </div>
          <div className = "control">
            <button className="button is-link">View</button>
          </div>
        </div>            
      </form>
      {status === 'fetched' &&
        <div className="columns">
          <div className= "column is-one-quarter">
            <div className="card">
              <div className="card-header">
              <p className="card-header-title">Ability Scores</p>
              </div>
              <div className="card-content">
                  {sheet.ability_scores.map((abil_score) => 
                    <p>
                      {abil_score.ability.name} {abil_score.score} ({Math.floor((abil_score.score -10) / 2)})
                    </p>
                  )}
                  <p>passive perception: {sheet.proficiency_bonus + 10} need to add wisome still</p>
                  <p>{sheet.proficiencies}</p>
              </div>

            </div>
          </div>
          <div className = "column is-one-quarter">
            <div className="card">
              <div className="card-content">
                <p>Prof bonus: +{sheet.proficiency_bonus}</p>
                <p>Saving Throws:</p>
                <ul>
                  {sheet.saving_throws.map((st) => <li>{st.ability.name} Saving {st.modifier} {st.proficient && <span>Is proficient</span>}</li>)}              
                </ul>
                <p>Skills:</p>
                <ul>
                  {sheet.skills.map((skill) => <li>{skill.skill.name} {skill.modifier} {skill.proficient && <span>Is proficient</span>}</li>)}
                </ul>
              </div>
            </div>
          </div>
          <div className = "column is-one-quarter">
            <div className = "card">
              <div className = "card-content">
                <p>Max health: {sheet.max_health}</p>
                <p>Speed: {sheet.speed}</p>
                <p>AC: {sheet.armour_class}</p>
                <p>Initative: {sheet.initiative_bonus}</p>
                <p>Hit dies: {sheet.hit_die}</p>
                <p>Weapons:</p>
                <p>{sheet.weapons}</p>
                <p>Equipment: </p>
                <p>{sheet.equipment}</p>
              </div>
            </div>
          </div>
          <div className = "column is-one-quarter"> 
          <div className="card">
            <div className="card-content">
              <p>Features:</p>
              <p>{sheet.features_traits}</p>
            </div>
          </div>
          </div>
        </div>
      }
    </>
  )
}


export default StatSheet