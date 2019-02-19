from flask import Flask, render_template, url_for, request
from ted_engine import ted_engine

app = Flask(__name__)
ted = ted_engine()
result = []

@app.route("/")
def home():
	return render_template('index.html', data = ted.tedData, result = result)

@app.route("/", methods=['POST'])
def search_form():
	search = request.form['search']
	result = ted.search(search)
	return render_template('index.html', data = ted.tedData, result = result, scroll='found')

if __name__ == '__main__':
	app.run(debug=True)