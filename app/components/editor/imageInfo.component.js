import React, { Component } from 'react'
// import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import { format } from 'date-fns'

class ImageInfo extends Component {
  constructor(props){
    super()
  }
  render(){
    const image = this.props.image
    if (! image) return null
    // const tags = (image.tags || "").split(",").map((s, i) => {
    //   return (
    //     <div className='pill' key={i}>
    //       {s.trim()}
    //     </div>
    //   )
    // })
    const tag_count = (image.regions || []).length

    const username = image.user ? image.user.username : "unknown"
    const date = format(image.created_at, 'DD-MMM-YYYY HH:mm')

    return (
      <div className='imageInfo'>
        <div className='filename'>{image.original_fn}</div>
        <div>
          uploaded by {username} on {date}
        </div>
        {image.graphic ? <span className='graphic'>contains graphic content</span> : null}
        <div>{image.description}</div>
        <Link className='' to={"/images/edit/" + image.id}>Edit Metadata</Link>
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => ({
  image: state.image.image,
});

const mapDispatchToProps = (dispatch) => ({
});

export default connect(mapStateToProps, mapDispatchToProps)(ImageInfo);
