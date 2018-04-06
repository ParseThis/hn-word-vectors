import io
import bz2
import logging
from os import path
import os
import random
from collections import defaultdict
import pdb
import plac
try:
    import ujson as json
except ImportError:
    import json
from gensim.models import Word2Vec
from preshed.counter import PreshCounter
from spacy.strings import hash_string
import gzip
from nltk import word_tokenize
from nltk import download
from utils import preprocess

logger = logging.getLogger(__name__)

from itertools import tee


# I got these helpers https://github.com/explosion/sense2vec
# which I forked to get to work with Spacy 2.0.

class Corpus(object):
    def __init__(self, directory, min_freq=10):
        self.directory = directory

    def __iter__(self):
        for text_loc in iter_dir(self.directory):
            with io.open(text_loc, 'r', encoding='utf8',errors='ignore') as file_:
                next(file_) # skip header
                for sent_str in file_:
                    yield preprocess(sent_str)



def iter_dir(loc):
    for fn in os.listdir(loc):
        if path.isdir(path.join(loc, fn)):
            for sub in os.listdir(path.join(loc, fn)):
                yield path.join(loc, fn, sub)
        else:
            yield path.join(loc, fn)

@plac.annotations(
    in_dir=("Location of input directory"),
    out_loc=("Location of output file"),
    n_workers=("Number of workers", "option", "n", int),
    size=("Dimension of the word vectors", "option", "d", int),
    window=("Context window size", "option", "w", int),
    min_count=("Min count", "option", "m", int),
    negative=("Number of negative samples", "option", "g", int),
    nr_iter=("Number of iterations", "option", "i", int),
)
def main(in_dir, out_loc, negative=5, n_workers=4, window=3, size=128, min_count=5, nr_iter=2):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    model = FastText(
        size=size,
        window=window,
        min_count=min_count,
        workers=n_workers,
        sample=1e-5,
        negative=negative
    )
    corpus = Corpus(in_dir)
    model.iter = nr_iter
    model.build_vocab(corpus)
    model.train(Corpus(in_dir), total_examples=model.corpus_count, epochs=model.iter)
    model.save(out_loc)


if __name__ == '__main__':
    plac.call(main)
