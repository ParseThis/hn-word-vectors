import sys
from gensim.models import Word2Vec
from utils import preprocess
import logging

logger = logging.getLogger(__name__)
def make_args():
	# TODO use argparse in the future
	pass

def main():
	infile, outfile, model_in  = sys.argv[1:4]
	model = Word2Vec.load(model_in)
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	with open(outfile, 'wb') as f: 
		for i, text in enumerate(open(infile)):
			words = preprocess(text)
			for word in words:
				try:
					vec = model.wv[word]
					# asset that  vec is  an array of 
					# 64 bit floats.
					vec_string = ' '.join(str(v) for v in vec)
					line = '{} {}'.format(word, vec_string) + '\n'
					f.write(line.encode())
				except KeyError as ex:
					continue
			if i % 1000 == 0 and i!=0:
				logger.info('Finished writing 1000 words')


if __name__ == '__main__':
	main()