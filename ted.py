from flask import Flask, render_template, url_for, request
from ted_engine import ted_engine

app = Flask(__name__)
ted = ted_engine()
result = []

@app.route("/")
def home():
	return render_template('index.html', data = ted.tedData, result = result, search = False)

@app.route("/", methods=['POST'])
def search_form():
	search = request.form['search']
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

	for link in url:
		embed_url.append(link.replace("www", "embed", 1))

	return render_template('index.html', data = ted.tedData, result = documents, scroll='found', title = title, url = embed_url, description = description, author = author, search = True)

if __name__ == '__main__':
	app.run(debug=True)