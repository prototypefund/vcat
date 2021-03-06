import { format } from 'date-fns'
import stringify from 'csv-stringify'
import saveAs from 'file-saver'

import * as types from '../types'
import { post, verify } from '../util'

import { getSavedFromStore, getCountFromStore, getSavedUrls } from './review.cache'

const url = {
  createNewGroup: () => '/api/images/import/new/'
}

const loading = (tag) => ({
  type: types.metadata.loading,
  tag
})
const loaded = (tag, data = {}) => ({
  type: types.metadata.loaded,
  tag,
  data
})
const error = (tag, err) => ({
  type: types.metadata.error,
  tag,
  err
})

// add a hash/frame to the reviewer
export const save = opt => dispatch => {
  console.log('save', opt)
  let saved = getSavedFromStore()
  let hash = saved[opt.hash] || {
    frames: {},
    hash: opt.hash,
    verified: opt.verified,
  }
  if (opt.frame) {
    hash.frames[parseInt(opt.frame, 10)] = true
  }
  hash.verified = opt.verified
  saved[opt.hash] = hash
  dispatch({ type: types.review.save, saved })
  dispatch({ type: types.review.dedupe, payload: false })
}

// mark a frame as being not for export
export const unsave = (opt) => dispatch => {
  console.log('unsave', opt)
  let saved = getSavedFromStore()
  let hash = saved[opt.hash]
  if (hash) {
    if (opt.frame && hash.frames[parseInt(opt.frame, 10)]) {
      hash.frames[parseInt(opt.frame, 10)] = false
    }
  }
  dispatch({ type: types.review.unsave, saved })
}

export const toggleSaved = (opt) => dispatch => {
  let { hash, frame } = opt
  let saved = getSavedFromStore()
  let el = saved[hash]
  let isSaved = false
  console.log(saved, el)
  if (el) {
    if (frame && el.frames && el.frames[parseInt(frame, 10)]) {
      isSaved = el.frames[parseInt(frame, 10)]
    }
  }
  console.log(isSaved)
  if (isSaved) {
    unsave(opt)(dispatch)
  } else {
    save(opt)(dispatch)
  }
}

// refresh the stored frames
export const refresh = () => dispatch => {
  let saved = getSavedFromStore()
  Object.keys(saved).forEach(key => {
    const hash = saved[key]
    let deleted = 0
    const frames = Object.keys(hash.frames)
    frames.forEach(frame => {
      if (!hash.frames[frame]) {
        delete hash.frames[frame]
        deleted += 1
      }
    })
    if (!frames.length || frames.length === deleted) {
      delete saved[key]
    }
  })
  dispatch({ type: types.review.refresh, saved })
}

// clear the stored frames
export const clear = () => dispatch => {
  dispatch({ type: types.review.clear })
}

// export a CSV of the stored sha256's
export const exportCSV = () => dispatch => {
  console.log('export CSV')
  let saved = getSavedFromStore()
  const results = Object.keys(saved).sort().map(key => {
    const { verified, hash, frames } = saved[key]
    return [
      hash,
      Object.keys(frames).join(', '),
      verify(verified),
    ]
  })
  stringify(results, (err, csv) => {
    const blob = new Blob([csv], {
      type: 'text/csv'
    })
    saveAs(blob, 'vsearch_investigation_' + format(new Date(), 'YYYYMMDD_HHmm') + '.csv')
    dispatch(loaded('csv', { count: results.length }))
  })
}

// check duplicates in current database using phash
export const dedupe = () => dispatch => {
  dispatch(loading('dedupe'))
  return new Promise((resolve, reject) => {
    const urls = getSavedUrls()
    post(process.env.VCAT_HOST + '/api/images/import/search/', {
      urls,
    }).then(res => {
      const { good, bad } = res
      let saved = getSavedFromStore()
      let count = 0
      bad.forEach(({ image }) => {
        console.log(image)
        const { sa_hash: hash, frame } = image
        const frameIndex = parseInt(frame, 10)
        if (saved[hash] && saved[hash].frames[frameIndex]) {
          saved[hash].frames[frameIndex] = false
          count += 1
        }
      })
      dispatch({ type: types.review.save, saved })
      dispatch({ type: types.review.dedupe, payload: true })
      resolve(good, bad)
    }).catch(err => {
      dispatch({ type: types.review.dedupe, payload: false })
      reject(err)
    })
  })
}

// submit the new group
export const create = ({ title, graphic }) => dispatch => {
  const urls = getSavedUrls()
  if (!title) return dispatch(error('create', 'No title'))
  if (!urls) return dispatch(error('create', 'No images to save'))
  dispatch(loading('create'))
  return post(url.createNewGroup(), {
    title,
    graphic,
    urls,
  }).then(res => {
    dispatch(loaded('create'))
    // clear()
    window.location.href = '/groups/show/' + res.image_group.id
  }).catch(res => {
    dispatch(error('create'))
    console.log(res)
  })
}
