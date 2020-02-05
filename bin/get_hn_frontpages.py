import json 
import requests 
import grequests 
import re

# match timestamps
TIMESTAMP_RE = re.compile(r'(?<=\/\s)20\d+')

class IterUrls:
    def __init__(self, fname):
        self.fname = fname

    @staticmethod
    def _parse_log(text):
        timestamp = re.match(TIMESTAMP_RE, text)
        if not timestamp:
            return 
        return timestamp.group()

    @staticmethod
    def _make_url(timestamp):
        return  'http://web.archive.org/werb/{timestamp}/http://www.news.ycombinator.com:80'

    def __iter__(self):
        with open(fname) as f:
            for log in f:
                url = IterUrls._make_url_
                timestamp = IterUrls._parse_log(log)
                if timestamp:
                    yield timestamp

if __name__ == '__main__':
    
    session = requests.Session()
    # default max pool size = 10
    # which right were I think is reasonable
    # adapter = requests.adapters.HTTPAdapter(pool_maxsize=(MAX_POOL_SIZE)

    # make N requests effectively in parallel

    fname = sys.argv[1] # use argparse
    urls = IterUrls(fname)

    
    



