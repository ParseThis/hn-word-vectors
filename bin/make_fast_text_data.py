import os.path
from utils import preprocess
HOME = os.path.join(os.path.expanduser("~"), 
                    'hacker-news-link-study', 'data', 'full-news')

if __name__ == "__main__":
	with open(HOME + '/titles_together.txt', 'w') as out_:
		with open(HOME + '/titles.txt') as in_:
			for x in in_:
				clean = preprocess(x) + ' '
				out_.write(clean)
