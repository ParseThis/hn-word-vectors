import sys
from gensim.models import Phrases
import logging

logger = logging.getLogger(__name__)


# train a phrases model to so that there could 
# be phrases in the word embeddings. 

class Corpus(object):
	def __init__(self, in_dir):
		self.file = in_dir
	def __iter__(self):
		with open(self.file, encoding='utf-8') as f:
			for line in f:
				yield line

def main():
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	in_dir, model_out = sys.argv[1:]
	sentences = Corpus(in_dir)
	phrases = Phrases(sentences)
	phrases.save(model_out)


if __name__ == "__main__":
	main()