import sys
import json
import argparse
import numpy as np
import tensorflow_hub as hub
import pandas as pd
from datetime import timedelta


# couldn't figure out how to get Pool work with 
# the Module class
# from multiprocessing import Pool
from sklearn.metrics.pairwise import cosine_similarity


CHUNKSIZE    = 10
POOLSIZE     = 2
WINDOW_SIZE  = 5
CHUNKSIZE    = WINDOW_SIZE * 1000
TIME_WINDOW  = timedelta(hours=12)
THRESH_END   = 0.95
THRESH_START = 0.6
MIN_SCORE   = 20

def compute_most_similar_titles_for_chunk(chunk):
    _embeddings = embed(chunk['title'].values)
    _sim_matrix = cosine_similarity(_embeddings)
    _ut = np.triu(_sim_matrix, k=1)
    _ind = np.unravel_index(np.argmax(_ut, axis=None), 
                                 shape=_ut.shape)
    return chunk.iloc[list(_ind)], _sim_matrix[_ind]

def get_similarity_record(r):
    m, sim_score = r
    delta = m.timestamp.diff()[1:]
    pair_score_gt_than_thresh = (m.score >= MIN_SCORE).all()
    return {'matches' : [(d.title, d.timestamp, d.score)
                          for d in m.itertuples()],
            'sim_score' :sim_score,
            'pair_score_gt_than_thresh' : pair_score_gt_than_thresh,
            'timedelta' : delta}

def compute_similarity(data, size):
    for chunk in chunker(data, size):
        yield compute_most_similar_titles_for_chunk(chunk)

def chunker(x, size):
    for i in range(0, len(x), size):
         yield x.iloc[i:i+size]


def filter_records(data):
    return 

def create_stats(data):
    return
                
            
if __name__ == '__main__':

    fname = './data/hn-posts.json'
    use_fname = './notebooks/use'
    embed = hub.load(use_fname)
    data = pd.read_json(fname, chunksize=CHUNKSIZE, lines=True)
   
    for batch in data: 
        for chunk in chunker(batch, size=WINDOW_SIZE):
            res = compute_most_similar_titles_for_chunk(chunk)
            record = get_similarity_record(res)
            score = record['sim_score']
            if (record['timedelta'] < TIME_WINDOW).all() \
                and score > THRESH_START and score < THRESH_END\
                and record['pair_score_gt_than_thresh']:
                print(record)
