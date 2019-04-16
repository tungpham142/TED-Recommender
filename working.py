import math
import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import defaultdict
	
def count_document(document, c):
	document_in_c = 0
	for doc in document:
		if c in doc:
			document_in_c += 1
	return document_in_c

def concatenate_text(categories, document, c):
	text_in_c = []
	for i in range(len(document)):
		if c in categories[i]:
			text_in_c.extend(document[i])
	
	return text_in_c

tedData = pd.read_csv('ted-data.csv')

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

stops = stopwords.words('english')

stemmer = PorterStemmer()

total_words = []

final_document = []

weight_vectors = []

vocabulary = []

categories = []

prior = {}

condprob = defaultdict(dict)

for i in range(len(tedData)):
	tokens = tokenizer.tokenize(tedData['title'][i])
	tokens += tokenizer.tokenize(tedData['description'][i])
	#tokens += tokenizer.tokenize(tedData['main_speaker'][i])
	'''
	transcript = tedData['transcript'][i]	
	if(isinstance(transcript, float) and  math.isnan(transcript)):
		transcript = ''

	tokens += tokenizer.tokenize(transcript)
	'''
	# Remove stop words
	final_tokens = []

	for token in tokens: 
		token = token.lower()
		if token not in stops:
			token = stemmer.stem(token)
			final_tokens.append(token) 
			if token not in vocabulary:
				vocabulary.append(token)
	final_document.append(final_tokens)


total_document = len(final_document)

total_term = len(vocabulary)

ratings = tedData['ratings']

for rating in ratings:
	if rating not in categories:
		categories.append(rating)

for c in categories:
	# Count how many documents are in class c
	document_in_c = count_document(ratings, c)
	prior[c] = document_in_c/float(total_document)
	# Concatenate all the text of class c in one list
	text_in_c = concatenate_text(ratings, final_document, c)

	for term in vocabulary:
		# Count how many term t are in class c
		Tct = text_in_c.count(term)
		condprob[term][c] = (Tct + 1)/(len(text_in_c) + total_term)

test = "mandfgbrt s hrst jf"
test_vocab = []
terms = tokenizer.tokenize(test)
for term in terms:
	term = term.lower()
	if term not in stops:
		term = stemmer.stem(term)
		test_vocab.append(term) 

score = {}
for c in categories:
	score[c] = prior[c]
	for term in test_vocab:
		if term in condprob:
			score[c] *= condprob[term][c]


total_score = sum(score.values())
print(total_score)
for c in sorted(score, key=score.get, reverse=True):
	print(c)
	print(score[c]/float(total_score))
	#print(s.values()/sum(score.values()))
