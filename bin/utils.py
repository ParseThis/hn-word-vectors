 import re
# from nltk.tokenize import TweetTokenizer
# from gensim.models import Phrases, phrases

# do this if  you want to use the a  gensim phrase model
# to infer phrases from the sequences. I haven't really
# found to work for the hackernews titles but I'm mostly
# likely missing something.

# MODEL_FILE = os.path.join(os.path.expanduser('~'), 'hn-word-vectors/models', 'phrases.model')
# phrases_model = Phrases.load(MODEL_FILE)
# bigrams = phrases.Phraser(phrases_model)


replace_numbers = re.compile(r'\d')
punks = re.compile(r'[|\+?{1[.,\/!@$%\^&\*;:{}=\-_`~\\"\'()]')
extra_spaces = re.compile(r'\s{2,}')
# tkn = TweetTokenizer()




def preprocess(text):

	text = text.strip().lower()
	text = re.sub(replace_numbers, '#', text)
	text = re.sub(punks, ' ', text)
	text = re.sub(extra_spaces, ' ', text)
	# text  = phrases[text]
	# return text
	return text
	



if __name__ == '__main__':

	text = '   THE name p3df /&&$(#*)(@@#$ will orson+adams ( climb the "wall"'
	print(processed, 'PROCESSED')
	processed = preprocess(text)
	# assert  processed == ['the', 'name', 'p#df', '#', '#', 'will', 'orson', 'adams', 'climb', 'the', 'wall']
