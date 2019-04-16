import pandas as pd
import re

def find_class(rates):
	count = []
	i = 5
	while(i < len(rates)):
		count.append(int(rates[i]))
		i = i + 6

	maxVote = max(count)
	index = count.index(maxVote) + 1
	categoryID = int(rates[index*6 - 5])

	while(categoryID > 10):
		count[index-1] = -1
		maxVote = max(count)
		index = count.index(maxVote) + 1
		categoryID = int(rates[index*6 - 5])

	category = rates[index*6 - 3].replace(' ','')
	return category

tedData = pd.read_csv('ted_data.csv')

ratings = tedData['ratings']
categories = []

for rating in ratings:
	rating = rating.replace('\'', '')
	rating = rating.replace('{', '')
	rating = rating.replace('}', '')
	rating = rating.replace('[', '')
	rating = rating.replace(']', '')
	rates = re.split(', |:', rating)

	category = find_class(rates) 
	categories.append(category)

tedData['ratings'] = categories
tedData.to_csv('ted-data.csv', index=False)

