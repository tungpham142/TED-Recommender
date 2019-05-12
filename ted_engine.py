# Core Engine for Ted-Recommneder Search feature
# Perform search on given query using TF-IDF weight to return ranked documents
# Return related documents not only by their titles, but by their contexts
# Perfrom classification on given query using Naive Bayes to returned belonged classes and its percentage
# The complete appication is hosted at Ted-Recommender.com

import math
import pandas as pd
import numpy
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

class ted_engine:
	# Needed attributes
	tedData = pd.read_csv('ted-data.csv')
	tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
	stops = stopwords.words('english')
	stemmer = PorterStemmer()
	total_words = []
	final_document = []
	weight_vectors = []
	posting_lists = {}
	vocabulary = []
	categories = []
	prior = {}
	condprob = defaultdict(dict)

	def __init__(self):		
		tedData = self.tedData
		tokenizer = self.tokenizer
		stops = self.stops
		stemmer = self.stemmer
		final_document = self.final_document
		weight_vectors = self.weight_vectors
		posting_lists = self.posting_lists
		vocabulary = self.vocabulary
		categories = self.categories
		prior = self.prior
		condprob = self.condprob

		for i in range(len(tedData)):
			tokens = tokenizer.tokenize(tedData['title'][i])
			tokens += tokenizer.tokenize(tedData['description'][i])
			tokens += tokenizer.tokenize(tedData['main_speaker'][i])
			tokens += tokenizer.tokenize(tedData['name'][i])
			tokens += tokenizer.tokenize(tedData['ratings'][i])
			tokens += tokenizer.tokenize(tedData['tags'][i])
			
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

		for document in final_document:
		 	weight_vector = {}
		 	for term in document:
		 		if term not in weight_vector:			
		 			tf = document.count(term)/len(document)
		 			df = sum(1 for document in final_document if term in document)
		 			n = len(final_document)
		 			weight = tf * math.log(n/df)
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

		# construct conditional prob. for naive bayes
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
				query_weight[term] = tf

		sim = {}
		for term in query_weight:
			if term in self.posting_lists:
				for post in self.posting_lists[term]:
					document = post[0]
					if document not in sim:
						sim[document] = 0
					sim[document] += post[1] * query_weight[term]
		sim = sorted(sim, key=sim.get, reverse=True)
		print(sim)
		return sim 

	def classify(self, query):
		query_vocab = []
		terms = self.tokenizer.tokenize(query)
		for term in terms:
			term = term.lower()
			if term not in self.stops:
				term = self.stemmer.stem(term)
				query_vocab.append(term) 

		score = {}
		for c in self.categories:
			score[c] = self.prior[c]
			for term in query_vocab:
				if term in self.condprob:
					score[c] *= self.condprob[term][c]


		total_score = sum(score.values())
		classification = {}
		for c in sorted(score, key=score.get, reverse=True):
			classification[c]= score[c]/float(total_score)
		return classification

	def recommend(self, docId, query):
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
				query_weight[term] = tf

		sim = {}
		for term in query_weight:
			if term in self.posting_lists:
				for post in self.posting_lists[term]:
					document = post[0]
					if document not in sim:
						sim[document] = 0
					sim[document] += post[1] * query_weight[term]
		sim.pop(docId)
		sim = sorted(sim, key=sim.get, reverse=True)
		print(sim)
		return sim 