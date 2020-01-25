import json
import tensorflow_hub as hub

class IterPosts:

    def __init__(fname, size):
        self.fname = fname
        self.size =  size
    def __iter__(self):
        data = map(json.loads, open(self.fname))
        chunk = []
        for i, d in enumerate(data):
            if i >= self.size:
                yield chunk
                chunk = []
            else:
                chunk.append(d)
        # if this i % 5 != 0 then
        # there are still elements in chunk
        # after the loop above
        if chunk:
            yield chunk

def _embed_update(chunk):
    embeddings = embed([c['title'] for c in chunk])
    for c, e in zip(chunk, embeddings):
        c.update({'embeddings' : e})
        yield c 

if __name__ == '__main__':


    embedded = []
    chunks = IterPosts(fname, 10000)
    for chunk in chunks:
        embedded.extend(_embed_update(chunk))
    with open(outfile, 'w') as out:
        json.dumps(embedded, out)


