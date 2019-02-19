import math
import pandas as pd
import numpy
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download()

class ted_engine:
	# Needed attributes
	tedData = pd.read_csv('ted_data.csv')
	tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
	stops = stopwords.words('english')
	stemmer = PorterStemmer()
	total_words = []
	final_document = []
	weight_vectors = []
	posting_lists = {}

	def __init__(self):		
		tedData = self.tedData
		tokenizer = self.tokenizer
		stops = self.stops
		stemmer = self.stemmer
		total_words = self.total_words
		final_document = self.final_document
		weight_vectors = self.weight_vectors
		posting_lists = self.posting_lists

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
					df = sum(1 for document in final_document if term in document)
					n = len(final_document)
					'''
					idf = math.log(len(final_document) / (1 + containing))
					'''
					weight = (1 + math.log10(tf)) * (math.log10(n/df))
					weight_vector[term] = weight

			weight_vectors.append(weight_vector)

		# construct posting lists
		for i in range(len(weight_vectors)):
			document = weight_vectors[i]
			for token in document:
				if token not in posting_lists:
					posting_lists[token] = []
				posting_lists[token].append([i, document[token]])
				posting_lists[token] = sorted(posting_lists[token], key=lambda x: x[1], reverse=True)

	def search(self, query):
		q = self.tokenizer.tokenize(query)
		tokens = []
		query_weight = {}
		for t in q:
			t = t.lower()
			if t not in self.stops:
				t = self.stemmer.stem(t) 
				tokens.append(t)

		for term in tokens:
			if term not in query_weight:
				tf = tokens.count(term) / len(tokens)
				w = (1 + math.log10(tf))
				query_weight[term] = w

		sim = {}
		for term in query_weight:
			if term in self.posting_lists:
				for post in self.posting_lists[term]:
					document = post[0]
					if document not in sim:
						sim[document] = 0
					sim[document] += post[1] * query_weight[term]
		sim = sorted(sim, key=sim.get, reverse=True)
		return sim
