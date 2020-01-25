import sys
import json
import argparse
import numpy as np
import tensorflow_hub as hub
import pandas as pd

from multiprocessing import Pool
from sklearn.metrics.pairwise import cosine_similarity


def compute_most_similar_titles_for_chunk(chunk):
    _embeddings = embed(chunk['title'].values)
    _sim_matrix = cosine_similarity(_embeddings)
    _ut = np.triu(_sim_matrix, k=1)
    _ind = np.unravel_index(np.argmax(_ut, axis=None), 
                                 shape=_ut.shape)
    return chunk.iloc[list(_ind)], _sim_matrix[_ind]

def get_similarity_record(r):
    m, sim_score = r
    delta = m.time.diff()[1:]
    return {'matches' : [(d.url, d.title, d.time, d.score)
                          for d in m.itertuples()],
            'sim_score' :sim_score, 
            'timedelta' : delta}




if __name__ == '__main__':

    fname = './data/links.csv'
    USE = './notebooks/use'

    CHUNKSIZE = 10
    POOLSIZE = 5
    embed = hub.load(USE)
    data = pd.read_csv(fname, chunksize=CHUNKSIZE)
    pool = Pool(POOLSIZE)
    
    for chunk in data:
        chunk.time = pd.to_datetime(chunk.time, unit='s')
        res = compute_most_similar_titles_for_chunk(chunk)
        print(get_similarity_record(res))
        
