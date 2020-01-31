import sys
import json
from multiprocessing import Pool
import numpy as np
from datetime import timedelta, datetime
from sklearn.metrics.pairwise import cosine_similarity
from compute_embeddings import IterPosts

CHUNKSIZE    = 10
POOLSIZE     = 5
WINDOW_SIZE  = 5
CHUNKSIZE    = WINDOW_SIZE * 1000
THRESH_END   = 0.95
THRESH_START = 0.6
MIN_SCORE   = 20


[1, 0, 0]
[0 ,1, 0]
[0, 0, 1]

def compute_most_similar_titles_for_chunk(chunk):
    """
         compute the max similarity index by 
         looking at the upper triangle
         not considering the main diag which 
         are a title's similarity with itself
    """
    embeddings = np.vstack([c['embeddings'] for c in chunk])
    sim_matrix = cosine_similarity(embeddings)
    ut = np.triu(sim_matrix, k=1)
    ind = np.unravel_index(np.argmax(ut, axis=None), shape=ut.shape)
    matches = chunk[ind[0]], chunk[ind[1]] 
    similarity = sim_matrix[ind]
    return  matches, similarity

def get_similarity_record(r):
    # dateformat datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'
    m, sim_score = r
    begin = datetime.strptime(m[0]['timestamp'], '%Y-%m-%d %H:%M:%S UTC')
    end = datetime.strptime(m[1]['timestamp'],   '%Y-%m-%d %H:%M:%S UTC')
    time_between_posts = begin - end
    return {'matches' : m, 
            'sim_score' :sim_score,
            'delta' : time_between_posts.total_seconds()}

def chunker(x, size):
    for i in range(0, len(x), size):
         yield x[i:i+size]


            
if __name__ == '__main__':
    
    # time in hours 
    time = sys.argv[1]
    TIME_WINDOW = timedelta(hours=int(time))
    fname = '../data/hn-posts-embedded.json'
    data = IterPosts(fname, size=CHUNKSIZE) 
    
    pool = Pool(2) 
    # grab a batch of data and for mini-batch (chunk) of WINDOW_SIZE
    # in the batch compute the two most similar titles
    
    num_similar_titles = 0
    rates = dict()
    for batch in data:
        for batch_id, res in enumerate(pool.imap_unordered(compute_most_similar_titles_for_chunk,
                                       chunker(batch, size=WINDOW_SIZE))):
            record = get_similarity_record(res)
            if not record:
                rates[batch_id] = 0
                continue
            else:
                # score = record['sim_score']
                # waht the proabablity that a use sees two 
                # similar posts with a specific window

                # what  is the density of similar posts within 
                # a specific window
                if (record['delta'] < TIME_WINDOW.total_seconds()):
                    rates[batch_id] = 1
        break

    print(rates)
