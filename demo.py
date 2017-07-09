    #!/usr/bin/env python3

'''
A class to test out the HTRC API
'''

import re
import requests
from hathitrust_api import DataAPI

class HTAPI(object):
    """A class to interact with the HT API, building on the library."""

    BIBLIO_URL = "http://catalog.hathitrust.org/api/volumes"

    def __init__(self, access_key, secret_key, output_dir='./'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.data_api = DataAPI(self.access_key, self.secret_key)
        self.OUTDIR = output_dir

    def download_workset(self, workset_file):
        """Download the OCR of each document in a workset"""
        workset = open(workset_file, 'r')
        next(workset)
        vids = [line.strip('\n').strip('"') for line in workset.readlines()]
        for vid in vids:
            self.download_bib(vid)
            self.download_doc(vid)

    def download_doc(self, vid):
        """Grab the text itself"""
        doc = self.data_api.getdocumentocr(vid)
        if len(doc) > 0:
            docstr = ''.join([line.decode('utf-8') for line in doc])
            out = open('{}/{}.txt'.format(self.OUTDIR, self.format_vid(vid)), 'w')
            out.write(docstr)
            out.close()

    def download_bib(self, vid, vid_type='htid', rec_type="brief"):
        """Grab the biblio"""
        url = "{}/{}/{}/{}.json".format(self.BIBLIO_URL, rec_type, vid_type, vid)
        rec = requests.get(url)
        out = open('{}/{}.json'.format(self.OUTDIR, self.format_vid(vid)), 'w')
        out.write(rec.text)
        out.close()

    def format_vid(self, vid):
        """Format vid for filenames"""
        return re.sub(r'[/ ]', '_', vid)

if __name__ == '__main__':

    ACCESS_KEY = 'e4d00e97ad'                   # OAUTH_CONSUMER_KEY
    SECRET_KEY = '17459d88803767e52c5435ad9f87' # OAUTH_CONSUMER_SECRET
    HT = HTAPI(ACCESS_KEY, SECRET_KEY, './download')
    HT.download_workset('epistemology-rca2t.csv')