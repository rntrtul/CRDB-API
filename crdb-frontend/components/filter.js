function FilterForm(){
  return (
    <div className = "field is-horizontal">
      <div className="field-label is-normal">
        <label className="label">Time Range</label>
      </div>
      <div className="field-body">
        <div className="field">
          <div className="control">
            <input className="input" type="text" placeholder="Min Time (HH:MM:SS)"/>
          </div>
        </div>
        <div className="field">
          <div className="control">
            <input className="input" type="text" placeholder="Max Time (HH:MM:SS)"/>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FilterForm