import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as actions from './review.actions'

class AnnotatorMenu extends Component {
  state = {
    title: '',
    graphic: false,
  }

  constructor() {
    super()
    this.handleInput = this.handleInput.bind(this)
  }

  handleInput(e) {
    let { name, value } = e.target
    if (name === 'title') {
      value = value.replace(/[^-_a-zA-Z0-9 ]/g, '')
    }
    if (name === 'graphic') {
      value = e.target.checked
    }
    this.setState({ [name]: value })
  }

  render() {
    return (
      <div className="importMenu">
        <div>
          <h3>New VCAT Image Group</h3>
          <label>
            <input
              type="text"
              name="title"
              placeholder="Title this group"
              onChange={this.handleInput}
              value={this.state.title}
            />
          </label>
          <label>
            <input
              type="checkbox"
              name="graphic"
              checked={this.state.graphic}
              onChange={this.handleInput}
            /> <small>Graphic content</small>
          </label>
          <label>
            <button
              className='btn check'
              onClick={this.props.actions.dedupe}>
              Dedupe
            </button>
            <button
              className='btn btn-primary create'
              onClick={this.props.actions.create}>
              Create Group
            </button>
          </label>
        </div>
      </div>
    )
  }
}

const mapStateToProps = state => ({
  review: state.review,
})

const mapDispatchToProps = dispatch => ({
  actions: bindActionCreators({ ...actions }, dispatch)
})

export default connect(mapStateToProps, mapDispatchToProps)(AnnotatorMenu)