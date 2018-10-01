#!python

import os
import sys
import argparse
import cv2 as cv
import simplejson as json
import ijson.backends.yajl2 as ijson

from django.core.management.base import BaseCommand, CommandError
from backend.vsearch.models import Document, DocumentTag

class Command(BaseCommand):
  help = 'Import metadata JSON files into the database'

  def add_arguments(self, parser):
    parser.add_argument('--dataset', required=True, type=str)
    parser.add_argument('--ijson', action='store_true')
    parser.add_argument('--unverified', action='store_true', default=False)

  def handle(self, *args, **options):
    self.stdout.write(str(options))
    verified = "unverified" if options['unverified'] else "verified"

    for tag in DocumentTag.objects.all():
      filename = "sis/datasets/{}/meta/{}/{}/index.json".format(options['dataset'], tag.name, verified)
      if not os.path.exists(filename):
        self.stdout.write("Not found: {}".format(filename))
        continue
      self.stdout.write("Importing {}".format(filename))
      with open(filename, 'r') as f:
        data = json.loads(f.read())
        index = 0
        for item in data.values():
          Document.objects.create(
            tag=tag,
            sha256=item['sha256'],
            data=json.dumps(item, separators=(',', ':'))
          )
          index += 1
          if (index % 1000) == 0:
            self.stdout.write("{}...".format(index))
      self.stdout.write(self.style.SUCCESS('Imported {}'.format(filename)))

# if we someday store binary sha256: int(item['sha256'], 16)