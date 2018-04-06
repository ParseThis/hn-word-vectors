import sys
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from utils import preprocess
import logging

PASSES =10

logger = logging.getLogger(__name__)

class TaggedDocuments(object):
    def __init__(self, filename):
        self.filename = filename
    def __iter__(self):
        for uid, line in enumerate(open(self.filename)):
        	doc = preprocess(line)
        	yield TaggedDocument(doc, tags=['SENT_%s' % uid])


def main():
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	in_file, model_out = sys.argv[1:]
	corpus = TaggedDocuments(in_file)
	model = Doc2Vec(alpha=0.025, min_alpha=0.025, min_count=1)  # use fixed learning rate
	# TODO Add shuffling of data set to each pass
	model.build_vocab(corpus)
	for epoch in range(PASSES):
		model.train(corpus, total_examples=model.corpus_count, epochs=1)
		model.alpha -= 0.002  # decrease the learning rate
		model.min_alpha = model.alpha  # fix the learning rate, no decay
	model.save(model_out)

if __name__ == '__main__':
	main()