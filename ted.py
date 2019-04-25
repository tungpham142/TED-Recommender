from flask import Flask, render_template, url_for, request
from ted_engine import ted_engine
import nltk

app = Flask(__name__)
ted = ted_engine()
result = []

@app.route("/")
def home():
	return render_template('index.html', data = ted.tedData, result = result, search = False)

@app.route("/", methods=['POST'])
def process():
	# Perform search
	search = search = request.form.get('search')
	if(search != None):
		result = ted.search(search)
		documents = []
		embed_url = []

		if(len(result) < 6):
			length = len(result)
		else:
			length = 6
		for i in range(length):
			documents.append(result[i])

		title = list(ted.tedData['title'][documents])
		url = list(ted.tedData['url'][documents])
		description = list(ted.tedData['description'][documents])
		author = list(ted.tedData['main_speaker'][documents])
		categories = list(ted.tedData['ratings'][documents])

		for link in url:
			embed_url.append(link.replace("www", "embed", 1))

		return render_template('index.html', data = ted.tedData, \
			result = documents, scroll='found', title = title, url = embed_url, \
			description = description, author = author, categories = categories, search = True)

	classify = search = request.form.get('classify')
	categories = []
	percentage = []
	if(classify != None):
		classification = ted.classify(classify)
		for c in classification:
			categories.append(c)
			percentage.append(round(classification[c] * 100, 2))
		return render_template('index.html', scroll='classification', categories = categories,\
			percentage = percentage, classification = classification, search = False)

if __name__ == '__main__':
	#app.run(debug=True)
	app.run(host="0.0.0.0", port="80")