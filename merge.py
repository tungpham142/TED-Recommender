import pandas as pd
import re

def find_class(rates):
	count = []
	i = 5
	while(i < len(rates)):
		count.append(rates[i])
		i = i + 6

	maxVote = max(count)
	index = count.index(maxVote) + 1
	categoryID = int(rates[index*6 - 5])
	print(categoryID)


	while(categoryID > 10):
		count[index-1] = -1
		maxVote = max(count)
		index = count.index(maxVote) + 1
		categoryID = int(rates[index*6 - 5])


tedData = pd.read_csv('ted_data.csv')

ratings = tedData['ratings']

for rating in ratings:
	rating = rating.replace('\'', '')
	rating = rating.replace('{', '')
	rating = rating.replace('}', '')
	rating = rating.replace('[', '')
	rating = rating.replace(']', '')
	rates = re.split(', |:', rating)

	find_class(rates)

