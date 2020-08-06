import React from "react"

class StatSheet extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isFetching: false,
      data: []
    }
  }

  fetchSheet() {
    this.setState({...this.state, isFetching: true})

    this.setState({...this.state, isFetching: false})
  }

  componentDidMount(){
    this.fetchSheet();
    this.timer = setInterval(() => this.fetchSheet(), 5000);
  }

  componentWillUnmount(){
    clearInterval(this.timer)
    this.timer = null
  }

  render(){
    return(
      <div>
        <h1>THIS IS A TEST YIPPPY</h1>
        <p>{this.state.isFetching ? 'loading...' : ''}</p>
      </div>
    )
  }
}