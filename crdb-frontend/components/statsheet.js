import { useFetch } from './fetcher'
import Link from 'next/link'
import React, { useState } from "react"

function slot_count(lvl, sheet){
  if (lvl === 1) return sheet.slots_one
  if (lvl === 2) return sheet.slots_two
  if (lvl === 3) return sheet.slots_three
  if (lvl === 4) return sheet.slots_four
  if (lvl === 5) return sheet.slots_five
  if (lvl === 6) return sheet.slots_six
  if (lvl === 7) return sheet.slots_seven
  if (lvl === 8) return sheet.slots_eight
  if (lvl === 9) return sheet.slots_nine
}

const StatSheet = (props) => {
  const [query, setQuery] = useState('');
  const url = query && `http://127.0.0.1:8000/characters/api/statsheet/${query}`
  const {status, data, error} = useFetch(url)
  
  const sheet = data
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    console.log(e.target.select)
		const query = e.target.select.value;
		if (query) {
      console.log(query)
			setQuery(query);
		}
  };  

  let levels = [1,2,3,4,5,6,7,8,9]
  // make the things into columns so one height doesn't affect other (look weird)
  return (
    <div className = "container">
    {props.data.length > 0 &&
    <form onSubmit={handleSubmit} className = "field">
      <div className="field is-grouped ">
        <div className="control">
          <div className ="select is-fullwidth">
            <select name="select">
              {props.data.map((sheet) =>
                <option key ={sheet.sheet_level} value={sheet.id}>Level {sheet.sheet_level}</option> 
              )}
            </select>
          </div>
        </div>
        <div className = "control">
          <button className="button is-link">View</button>
        </div>
      </div>            
    </form>
    }
    {props.data.length === 0 && 
      <div className = "has-text-centered">
        <p>No character sheets are currently available.</p>
      </div>
    }
    {status === 'fetched' &&
    <div>
      <div className = "tile is-ancestor">
        <div className = "tile is-parent is-6">
          <div className = "tile is-child box">
            <div className="level is-mobile">
              {sheet.ability_scores.map((abil_score) => 
                <div className="level-item has-text-centered">
                  <div>
                    <p className="heading">{abil_score.ability.name}</p>
                    <p className="title">{abil_score.score}</p>
                    <p className="subtitle">{Math.floor((abil_score.score - 10) / 2)}</p>
                  </div>
                </div>
              )}  
            </div>
          </div>
        </div>
        <div className = "tile is-parent is-1">
          <div className = "tile is-child box">
            <div className = "level">
            <div className = "level-item has-text-centered">
                <div>
                  <p className = "heading">AC</p>
                  <p className = "title">{sheet.armour_class}</p>
                </div>
              </div>
              
            </div>
          </div>
        </div>
        <div className = "tile is-parent is-5">
          <article className = "tile is-child box">
            <div className = "level">
              <div className = "level-item has-text-centered">
                <div>
                  <p className = "heading">Class{sheet.classes.length > 1 && <span>es</span>}</p>
                  <p className = "title"> 
                    {sheet.classes.map((cls, idx) => 
                      <span>
                        {cls.class_id.name} {cls.level}
                        {sheet.classes.length > 0 && idx < sheet.classes.length -1 && <span> / </span>} </span>
                    )}
                  </p>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
      

      <div className="tile is-ancestor">
        <div className = "tile is-parent is-vertical is-3"> 
          <div className="tile is-child box">
            <p><b>Saving Throws:</b></p>
            <table>
              <thead>
                <tr>
                  <th><abbr title="proficency">Prof</abbr></th>
                  <th>Ability</th>
                  <th>Mod</th>
                </tr>
              </thead>
              <tbody>
                {sheet.saving_throws.map((st) => 
                  <tr>
                    <td className="is-unselectable">{st.proficient === true && <span>&#9899;</span>}{st.proficient === false && <span>&#9898;</span>}</td>
                    <td>{st.ability.name}</td>
                    <td>{st.modifier}</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div> 
          
          <div className = "tile is-child box">
              <p><b>Profs and languages</b></p>
              <div>{sheet.proficiencies.split('\n').map((i, key) => {return <p key={key}>{i}</p>})}</div>
            </div>
        </div>
        <div className = "tile is-parent is-3">
          <article className = "tile is-child box">
            <p><b>Skills:</b></p>
            <table class = "table">
              <thead>
                <tr>
                  <th><abbr title="proficency">Prof</abbr></th>
                  <th>Skill</th>
                  <th>Mod</th>
                </tr>
              </thead>
              <tbody>
                {sheet.skills.map((skill) => 
                <tr>
                  <td className="is-unselectable">{skill.proficient === true && <span>&#9899;</span>}{skill.proficient === false && <span>&#9898;</span>}</td>
                  <td>{skill.skill.name}</td>
                  <td>{skill.modifier}</td>
                </tr>
              )}
            </tbody>
            </table>
            </article>
        </div>
      
        <div className = "tile is-vertical">
          <div className = "tile">
            <div className= "tile is-parent">
              <div className= "tile is-child box">
                <div className = "level">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className = "heading">Speed</p>
                      <p className = "title">{sheet.speed}</p>
                    </div>
                  </div>
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className = "heading">Prof Bonus</p>
                      <p className = "title">+{sheet.proficiency_bonus}</p>
                    </div>
                  </div>
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className = "heading">Initative</p>
                      <p className = "title">{sheet.initiative_bonus}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className = "tile is-parent">
              <article className = "tile is-child box">
                <div className = "level">
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className = "heading">Health</p>
                      <p className = "title">{sheet.max_health}</p>
                    </div>
                  </div>
                  <div className = "level-item has-text-centered">
                    <div>
                      <p className = "heading">Hit Dice</p>
                      <p className = "title">{sheet.hit_die}</p>
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </div>

          <div className = "tile is-parent">
            <div className = "tile is-child box" >
              <p><b>Feats & Traits:</b></p>
              <div>{sheet.features_traits.split('\n').map((i, key) => {return <p key={key}>{i}</p>})}</div>
            </div>

          </div>
          
          <div className="tile is-parent">
            <div className = "tile is-child box">
              <p><b>Equpiment</b></p>
              <p>Weapons:</p>
              <p>{sheet.weapons}</p>
              <p>Equipment: </p>
              <p>{sheet.equipment}</p>
            </div>
          </div>
        </div>
      </div>

      {sheet.learned_spells.length > 0 &&
       <div className = "tile is-ancestor">
        <div className = "tile is-parent">
          <div className = "tile is-child box">
              <div className = "level">
                <div className = "lefl-left">
                  <p><b>Spells</b></p>
                </div> 
                <div className = "level-right">
                  <div className = "level-item">
                    <div>
                      <p>Casting Class: {sheet.casting_class}</p>
                    </div>
                  </div>
                  <div className = "level-item">
                    <div>
                      <p>Spell Save DC: {sheet.spell_save}</p>
                    </div>
                  </div>
                  <div className = "level-item">
                    <div>
                      <p>Spell Attack Bonus: {sheet.spell_attack_bonus}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className = "columns">
              {levels.map((lvl) => 
                <div className= "column has-text-centered">
                  <div className = "level">
                    <div className = "level-item">
                      <div>
                        <p className= "title">{lvl}</p>
                        <p className= "heading">{slot_count(lvl,sheet)} slot{slot_count(lvl,sheet) > 1 && <span>s</span>}</p>
                      </div>
                    </div>
                  </div>
                  {sheet.learned_spells.map((ls) => 
                  <p>
                    {ls.spell.level === lvl && 
                    <Link href = "/spells/[id]" as={`/spells/${ls.spell.id}`}>
                      <a>{ls.spell.name}</a>
                    </Link>}
                  </p>)}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>}
    </div>}
    </div>
  )
}

export default StatSheet