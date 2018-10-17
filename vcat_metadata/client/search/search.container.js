import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import * as querystring from 'querystring'

import * as searchActions from './search.actions'
import * as metadataActions from '../metadata/metadata.actions'

import SearchQuery from './search.query'
import SearchResults from './search.results'

class SearchContainer extends Component {
  componentDidMount() {
    const qs = querystring.parse(this.props.location.search.substr(1))
    if (qs && qs.url) {
      this.props.searchActions.search(qs.url)
    } else {
      this.searchByHash()
    }
  }

  componentDidUpdate(prevProps) {
    if (prevProps.match.params !== this.props.match.params) {
      this.searchByHash()
    }
    // const qsOld = querystring.parse(prevProps.location.search.substr(1))
    // const qsNew = querystring.parse(this.props.location.search.substr(1))
    // if (qsOld && qsNew && qsNew.url && qsNew.url !== qsOld.url) {
    //   this.props.actions.search(qsNew.url)
    // }
  }

  searchByHash(offset = 0) {
    const { verified, hash, frame } = this.props.match.params
    if (verified && hash && frame) {
      this.props.searchActions.searchByVerifiedFrame(verified, hash, frame, offset)
    } else if (hash && frame) {
      this.props.searchActions.searchByFrame(hash, frame, offset)
    }
    if (hash && !offset) {
      this.props.metadataActions.fetchMetadata(hash)
    }
  }

  searchByOffset() {
    const offset = this.props.query.results.length
    this.searchByHash(offset)
  }

  render() {
    const { query, results, loadingMore } = this.props.query
    console.log(query, results, loadingMore)
    let showLoadMore = true
    if (!query || query.reset || query.loading || !results || !results.length) {
      showLoadMore = false
    }
    return (
      <div>
        <SearchQuery />
        <SearchResults />
        {showLoadMore
          ? !loadingMore
            ? <button
                onClick={() => this.searchByOffset()}
                className={(results && results.length > 50) ? 'btn loadMore wide' : 'btn loadMore'}
              >
                Load more
              </button>
            : <div className='loadingMore'>{'Loading more results...'}</div>
          : <div></div>
        }
      </div>
    )
  }
}

const mapStateToProps = state => ({
  query: state.search.query,
  options: state.search.options,
  metadata: state.metadata,
})

const mapDispatchToProps = dispatch => ({
  searchActions: bindActionCreators({ ...searchActions }, dispatch),
  metadataActions: bindActionCreators({ ...metadataActions }, dispatch),
})

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(SearchContainer))