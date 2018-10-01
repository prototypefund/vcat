import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
// import { Link } from 'react-router-dom'
import actions from '../../actions'
import { site } from '../../util/site'

import ImageGroupBrowser from '../imageGroup/imageGroupBrowser.component'
import UserStats from './userStats.component'

class StaffDashboard extends Component {
  constructor(props){
    super(props)
    props.actions.user.index()
    props.actions.hierarchy.index()
  }
  render(){
    return (
      <div className='dashboard'>
        <div className="columns">
          <div className="col4 dash-a">
            <div><img className="" alt='logo' src="/static/logo-large.png" /></div>
          </div>
          <div className="col1">
          &nbsp;
          </div>
          <div className="col7">
            <h1>Welcome to VCat</h1>
            <h2>{site.client_name}</h2>
            <UserStats />
          </div>
        </div>
        <br/><br/>

        <ImageGroupBrowser
          adminView
          title="All Image Groups"
          location={this.props.location}
        />
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => ({
  ...ownProps
})

const mapDispatchToProps = (dispatch) => ({
  actions: {
    imageGroup: bindActionCreators({ ...actions.imageGroup }, dispatch),
    image: bindActionCreators({ ...actions.image }, dispatch),
    hierarchy: bindActionCreators({ ...actions.hierarchy }, dispatch),
    user: bindActionCreators({ ...actions.user }, dispatch),
  },
})

export default connect(mapStateToProps, mapDispatchToProps)(StaffDashboard);
