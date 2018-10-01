#!python

from os import path
from pathlib import Path
from random import randint
import faiss
import sqlite3
import numpy as np
import sys

import os
realpath = os.path.realpath(sys.argv[0])
if 'faiss_db' in realpath:
  import config
else:
  import faiss_db.config

class FaissSearch:

  # Initialize the FAISS index and the SQLite database.
  def __init__(self, recipe, factory_type=None, index_fn=None):
    dataset = recipe.dataset
    factory_type = factory_type or recipe.faiss.factory_type

    base_dir = path.join(path.dirname(path.abspath(__file__)), "..")
    data_dir = path.join(base_dir, "datasets", dataset, "data")

    db_fn = path.join(base_dir, "datasets", dataset, "index", "sqlite3.db")
    if index_fn is None:
      index_fn = path.join(base_dir, "datasets", dataset, "index", "faiss-{}.index".format(factory_type.replace(',', '_')))
    else:
      index_fn = path.join(base_dir, "datasets", dataset, "index", index_fn)

    self.recipe = recipe
    self.db_fn = db_fn
    self.db = sqlite3.connect(db_fn)
    self.count = self.get_total_count()
    self.index = faiss.read_index(index_fn)
    self.pickle_files = list(Path(path.join(data_dir)).glob('*.pkl'))
    self.data_dir = data_dir
    self.pickle_fn = None
    self.pickle_data = None

  # Perform a search using a feature vector
  def search(self, query, offset=0, limit=15, size='sm'):
    if query is None:
      return []

    db = sqlite3.connect(self.db_fn)
    cursor = db.cursor()

    # note: it's possible to query FAISS with several vectors at once
    if len(query.shape) == 1:
      query = np.array([query])
    
    distances, indexes = self.index.search(query, offset + limit)

    if len(indexes) == 0:
      return []

    distances = distances[0]
    indexes = indexes[0]

    if offset > 0:
      distances = distances[offset:offset+limit]
      indexes = indexes[offset:offset+limit]

    if len(indexes) == 0:
      return []

    lookup = {}
    for _d, _i in zip(distances, indexes):
      lookup[_i+1] = _d

    if len(indexes) == 1:
      q = '''
          SELECT id, file, verified, hash, frame FROM frames WHERE id=?
      '''
      cursor.execute(q, (indexes[0]+1,))
    else:
      q = '''
          SELECT id, file, verified, hash, frame FROM frames WHERE id IN {}
      '''.format(tuple([_i+1 for _i in indexes]))
      cursor.execute(q)

    rows = cursor.fetchall()
    # print(rows)

    results = []
    for row in rows:
      if row[0] in lookup:
        results.append(self.format_match(row, distance=float(lookup[row[0]])))

    return sorted(results, key=lambda x: x['distance'])

  # Search using a frame from the database
  def search_by_frame(self, file, hash, frame, offset=0, limit=15):
    vec = self.load_feature_vector(file, hash, frame)
    return self.search(vec, offset=offset, limit=limit), self.format_match((file, hash, frame,))

  # Search using a random frame from the database
  def search_random(self, limit=15):
    id = randint(1, self.count)
    row = self.find_by_id(id)
    vec = self.load_feature_vector(row[0], row[1], row[2])
    return self.search(vec, limit=limit), self.format_match(row)

  # List frames in a video
  def browse(self, hash):
    db = sqlite3.connect(self.db_fn)
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, file, verified, hash, frame FROM frames WHERE hash=?
    ''', (hash,))

    rows = cursor.fetchall()
    # print(rows)

    results = []
    for row in rows:
      results.append(self.format_match(row))
    return results

  # Generate a mediarecord for a hash
  def mediarecord(self, hash):
    db = sqlite3.connect(self.db_fn)
    cursor = db.cursor()
    cursor.execute('''
        SELECT id, file, verified, hash, frame FROM frames WHERE hash=? LIMIT 1
    ''', (hash,))

    rows = cursor.fetchall()
    if len(rows) is 0:
      return {}

    row = rows[0]

    id, file, verified, hash, frame = row
    print(row)
    media_format = "video" if frame != -1 else "photo"
    verified_str = "verified" if verified == 1 else "unverified"

    return {
      "media_format": media_format,
      "sha256": hash,
      "verified": verified_str,
    }

  # Format the query for JSON output
  def format_match(self, row, distance=-1, size='sm'):
    if len(row) == 4:
      id = -1
      file, verified, hash, frame = row
    else:
      id, file, verified, hash, frame = row
    res = {
      'file': file,
      'verified': verified,
      'hash': hash,
      'frame': frame,
      'url': self.url_for(verified, hash, frame, size)
    }
    if id != -1:
      res['id'] = id
    if distance != -1:
      res['distance'] = distance
    return res

  # Count how many images are in the database
  def get_total_count(self):
    db = sqlite3.connect(self.db_fn)
    cursor = db.cursor()
    cursor.execute('SELECT Count(*) FROM frames')
    row = cursor.fetchone()
    return row[0]

  # Look up an image by ID
  def find_by_id(self, id):
    db = sqlite3.connect(self.db_fn)
    cursor = db.cursor()
    cursor.execute('SELECT file, verified, hash, frame FROM frames WHERE id=?', (id,))
    row = cursor.fetchone()
    return row

  # Generate a URL for a given image
  def url_for(self, verified, hash, frame='-1', size='sm'):
    if frame == '-1':
      if verified == 1:
        type = 'photos'
      else:
        type = 'unverified/photos'
      # todo: confirm photos endpoint
      url = "{}/v1/media/{}/{}/{}/{}/{}/{}/index.jpg".format(self.recipe.storage.endpoint, type, hash[0:3], hash[3:6], hash[6:9], hash, size)
    else:
      if verified == 1:
        type = 'keyframes'
      else:
        type = 'unverified/keyframes'
      url = "{}/v1/media/{}/{}/{}/{}/{}/{}/{}/index.jpg".format(self.recipe.storage.endpoint, type, hash[0:3], hash[3:6], hash[6:9], hash, frame, size)
    return url

  # Load a feature vector directly from the Pickle file.
  # Requires loading the entire pickle file...
  def load_feature_vector(self, file, hash, frame):
    if 0 > file or file > len(self.pickle_files):
      return None
    fn = self.pickle_files[file]
    if fn != self.pickle_fn:
      self.pickle_fn = fn
      self.pickle_data = config.load_pickle(self.data_dir, fn)
    if len(frame) != 6 and frame[0] != '0':
      vec = self.pickle_data['photos'][hash]
    else:
      vec = self.pickle_data['videos'][hash][frame]
    return vec
