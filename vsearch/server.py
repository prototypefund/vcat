#!python

import os
import sys
import json
import argparse
import cv2 as cv
import numpy as np
from datetime import datetime
from flask import Flask, request, render_template, jsonify
from PIL import Image  # todo: try to remove PIL dependency
import re

sanitize_re = re.compile('[\W]+')
valid_exts = ['.gif', '.jpg', '.jpeg', '.png']

from dotenv import load_dotenv
load_dotenv()

from faiss_db.db import FaissSearch
import faiss_db.config as config

from feature_extractor import FeatureExtractor

parser = argparse.ArgumentParser()
parser.add_argument('--config', default=os.getenv('FAISS_RECIPE'))
parser.add_argument('--factory_type')
opt = parser.parse_args()

recipe = config.load(opt.config)

dataset = recipe.dataset
factory_type = opt.factory_type or recipe.faiss.factory_type

fe = FeatureExtractor(config=recipe)
db = FaissSearch(recipe, factory_type, feature_extractor=fe)

DEFAULT_LIMIT = 50

# print(json.dumps(results, indent=2))

app = Flask(__name__, static_url_path="/search/static", static_folder="static")

# static api routes - this routing is actually handled in the JS
@app.route('/', methods=['GET'])
def index():
  return app.send_static_file('index.html')
@app.route('/search/', methods=['GET'])
def search_index():
  return app.send_static_file('index.html')
@app.route('/search/<path:path>', methods=['GET'])
def search_path(path):
  return app.send_static_file('index.html')
@app.route('/metadata/', methods=['GET'])
def metadata_index():
  return app.send_static_file('metadata.html')
@app.route('/metadata/<path:path>', methods=['GET'])
def metadata_path(path):
  return app.send_static_file('metadata.html')

# this is a vcat endpoint, included here as a no-op.
@app.route('/api/images/import/search/', methods=['POST'])
def import_():
    return jsonify({ 'good': [], 'bad': [] })

# query a mediarecord
@app.route('/search/api/mediarecord/<sha>', methods=['GET'])
def mediarecord(sha):
  return jsonify(db.mediarecord(sha) or { 'err': 'Hash not found' })

# list a directory
@app.route('/search/api/list/<sha>', methods=['GET'])
def list(sha):
  frames = db.browse(sha)
  return jsonify({
    'path': sha,
    'results': frames,
  })

# search using an uploaded file
@app.route('/search/api/upload', methods=['POST'])
def upload():
  try:
    limit = int(request.args.get('limit'))
  except:
    limit = DEFAULT_LIMIT
  file = request.files['query_img']
  fn = file.filename
  if fn.endswith('blob'):
    fn = 'filename.jpg'
  # how to refactor this to get it to
  basename, ext = os.path.splitext(fn)
  print("got {}, type {}".format(basename, ext))
  if ext.lower() not in valid_exts:
    return jsonify({ 'error': 'not an image' })

  uploaded_fn = datetime.now().isoformat() + "_" + basename
  uploaded_fn = sanitize_re.sub('', uploaded_fn)
  uploaded_img_path = "static/uploaded/" + uploaded_fn + ext
  uploaded_img_path = uploaded_img_path.lower()
  print('query: {}'.format(uploaded_img_path))

  img = Image.open(file.stream)
  img.save(uploaded_img_path)

  # query = db.load_feature_vector_from_file(uploaded_img_path)
  query = fe.extract(img)
  results = db.search(query, limit=limit)
  return jsonify({
    'query': { 'url': uploaded_img_path },
    'results': results,
  })

# search using a specific file from the database
# @app.route('/search/api/search/<int:file>/<hash>/<frame>', methods=['GET'])
# def search(file, hash, frame):
#   offset, limit = get_offset_and_limit()
#   results, query = db.search_by_frame(file, hash, frame, offset=offset, limit=limit)
#   return jsonify({
#     'query': query,
#     'results': results,
#   })

@app.route('/search/api/search/<hash>/<frame>', methods=['GET'])
def search(hash, frame):
  offset, limit = get_offset_and_limit()
  results, query = db.search_by_frame(hash, frame, offset=offset, limit=limit)
  return jsonify({
    'query': query,
    'results': results,
  })

# search using a random file from the database
@app.route('/search/api/random', methods=['GET'])
def random():
  offset, limit = get_offset_and_limit()
  results, query = db.search_random(limit=limit)
  return jsonify({
    'query': query,
    'results': results,
  })

# search using an external url
@app.route('/search/api/fetch/', methods=['GET'])
def fetch():
  offset, limit = get_offset_and_limit()
  url = request.args.get('url')
  if url.startswith('static'):
    print("loading file: {}".format(url))
    query = db.load_feature_vector_from_file(os.path.abspath(url))
    print(query.shape)
  else:
    print("fetching url: {}".format(url))
    query = db.load_feature_vector_from_url(url)
  results = db.search(query, offset=offset, limit=limit)
  return jsonify({
    'query': { 'url': url },
    'results': results,
  })

# tidy up search arguments
def get_offset_and_limit():
  try:
    limit = int(request.args.get('limit'))
  except:
    limit = DEFAULT_LIMIT
  try:
    offset = int(request.args.get('offset')) or 0
  except:
    offset = 0
  return offset, limit

if __name__=="__main__":
    app.run("0.0.0.0", debug=False)

