import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import actions from '../../actions'

import UserSelect from '../common/userSelect.component'
import Thumbnail from '../common/thumbnail.component'

class ImageGroupRow extends Component {
  constructor(){
    super()
    this.handleAssign = this.handleAssign.bind(this)
    this.handleDestroy = this.handleDestroy.bind(this)
  }
  handleAssign(e){
    let assigned_to = e.target.value
    const group = this.props.group
    if (!parseInt(assigned_to, 10)) {
      assigned_to = null
    }
    this.props.actions.imageGroup.update(group.id, { assigned_to })
  }
  handleDestroy(e){
    const group = this.props.group
    const imageCount = group.images.length
    let confirmMsg = "Really delete this group?"
    if (imageCount) {
      confirmMsg += "\n\nThis will also delete " + imageCount + " images."
    }
    const shouldDelete = window.confirm(confirmMsg)
    if (shouldDelete) {
      this.props.actions.imageGroup.destroy(group.id)
    }
  }
  render(){
    let { group, limit } = this.props
    if (!limit) limit = Infinity
    // console.log(group)
    const heading = group.from_sa ? group.sa_hash : group.source_url
    const images = group.images.slice(0, limit).map((el, i) => {
      return (
        <Link to={"/groups/show/" + group.id + "/annotate/" + el.id} key={i}>
          <Thumbnail
            key={i}
            type={'images'}
            node={el}
            showAnnotations
          />
        </Link>
      )
    })
    const limitedWarning = group.images.length > limit
    const notShownCount = group.images.length - limit
    let userSelect, buttons;
    if (this.props.adminView) {
      userSelect = (
        <UserSelect value={group.assigned_to} list={this.props.user.list} onChange={this.handleAssign} />
      )
      buttons = (
        <div className="column col-4 buttons">
          <span>{'Delete group'}</span>
          <button className="btn btn-sm btn-error" onClick={this.handleDestroy}>x</button>
        </div>
      )
    } else {
      buttons = (
        <div className="column col-4">
        </div>
      )
    }
    return (
      <div className="columns imageGroupRow">
        <div className="column col-8">
          <h5>
            {userSelect}
            <span>
              {'Group name: '}
              <Link to={"/groups/show/" + group.id}>{heading}</Link>
              {"(" + group.images.length + " image" + courtesyS(group.images.length) + ")"}
            </span>
          </h5>
        </div>
        {buttons}
        <div className="column col-12 gallery">
          {images}
          <div>
            {limitedWarning && (
              '+ ' + (notShownCount) + ' more image' + courtesyS(notShownCount) 
            )}
          </div>
        </div>
      </div>
    )
  }
}

const courtesyS = n => n !== 1 ? 's' : ''

const mapStateToProps = (state, ownProps) => ({
  ...ownProps,
  user: state.user,
})

const mapDispatchToProps = (dispatch) => ({
  actions: {
    imageGroup: bindActionCreators({ ...actions.imageGroup }, dispatch),
  },
})

export default connect(mapStateToProps, mapDispatchToProps)(ImageGroupRow);

