import math
import pandas as pd
import numpy
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

tedData = pd.read_csv('ted_data.csv')

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

stops = stopwords.words('english')

stemmer = PorterStemmer()

total_words = []

final_document = []

weight_vectors = []

for i in range(len(tedData)):
	tokens = tokenizer.tokenize(tedData['title'][i])
	# Add tokenize words to tokens
	'''
	tokens = tokenizer.tokenize(tedData['description'][i])
	tokens += tokenizer.tokenize(tedData['main_speaker'][i])
	tokens += tokenizer.tokenize(tedData['name'][i])
	tokens += tokenizer.tokenize(tedData['title'][i])
	
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
			final_tokens.append(stemmer.stem(token)) 
	final_document.append(final_tokens)

for document in final_document:
	weight_vector = {}
	for term in document:
		if term not in weight_vector:
			tf = document.count(term)/len(document)
			containing = sum(1 for document in final_document if term in document)
			idf = math.log(len(final_document) / (1 + containing))
			weight = tf * idf
			weight_vector[term] = weight

	weight_vectors.append(weight_vector)
print(weight_vectors)	

# construct posting lists
posting_lists = {}
for i in range(len(weight_vectors)):
	document = weight_vectors[i]
	for token in document:
		if token not in posting_lists:
			posting_lists[token] = [i, document[token]]
		else:
			posting_lists[token].append([i, document[token]])

		#posting_lists[token] = sorted(posting_lists[token], key=lambda post: post[2], reverse=True)

#print(posting_lists)



