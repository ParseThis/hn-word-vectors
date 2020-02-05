import sys
import os
import time
import json 
import grequests 
import requests 
import re

# match timestamps
TIMESTAMP_RE = re.compile(r'(?<=\/\s)20\d+')

class IterUrls:
    def __init__(self, fname):
        self.fname = fname

    @staticmethod
    def _parse_log(text):
        timestamp = re.search(TIMESTAMP_RE, text)
        if not timestamp:
            return 
        return timestamp.group().strip()

    @staticmethod
    def _make_url(timestamp):
        return f'http://web.archive.org/web/{timestamp}/http://www.news.ycombinator.com:80'

    def __iter__(self):
        with open(fname) as f:
            for log in f:
                timestamp = IterUrls._parse_log(log)
                if timestamp:
                    url = IterUrls._make_url(timestamp)
                    yield url

def _parse_response(response):

    if response.ok:
        return {'headers' : dict(response.headers),
                'content' : response.text}
    else:
        print(response.status_code)
        print(response.text)
        return 

if __name__ == '__main__':
    
    CHUNK = 50
    SLEEP = 60
    fname = sys.argv[1] # use argparse
    outdir = sys.argv[2]
    
    
    os.makedirs(outdir, exist_ok=True) 
    
  
    urls = (grequests.get(url) for url in IterUrls(fname))
    for i, response in enumerate(grequests.imap(urls)):
        parsed_response = _parse_response(response)
        if parsed_response:
            fname = parsed_response['headers'].get('x-cache-key',
                                                    'no-x-cache-key-' + str(i)
                                                   + '.json')
            fname = fname.replace('/', '-')
            fname = os.path.join(outdir, fname) 
            with open(fname, 'w') as  _out:
                print(f'Writing Response to file {fname}...')
                json.dump(parsed_response, _out)
            if i%CHUNK==0 and i!=0: 
                print('LAZY: Sleeping for a bit ...')
                time.sleep(SLEEP)
    



