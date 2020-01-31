import sys
import json
import numpy as np
import tensorflow_hub as hub

class IterPosts:
    def __init__(self, fname, size):
        self.fname = fname
        self.size =  size
    def __iter__(self):
        data = map(json.loads, open(self.fname))
        chunk = []
        for i, d in enumerate(data):
            if i % self.size == 0 and i != 0:
                yield chunk
                chunk = []
            else:
                chunk.append(d)
        # if this i % chunk at this point != 0 then
        # there are still elements in chunk
        # after the loop above yield that chunk
        if chunk:
            yield chunk

def _embed_update(chunk):
    titles = [c['title'] for c in chunk]
    embeddings = np.array(embed(titles)).tolist()
    for c, e in zip(chunk, embeddings):
        c.update({'embeddings' : e})
        yield json.dumps(c)

if __name__ == '__main__':

    CHUNKSIZE = 5000
    fname = './data/hn-posts.json'
    chunks = IterPosts(fname, CHUNKSIZE)
    outfile = './data/hn-posts-embedded.json'
    embed = hub.load('./notebooks/use')
    with open(outfile, 'w') as out:
        for i, chunk in enumerate(chunks):
            for em in _embed_update(chunk):
                out.write(em + '\n')
