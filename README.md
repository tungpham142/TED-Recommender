# TED-Recommender
[http://Ted-recommender.com](http://3.17.150.50)
Web Application built for reseach purpose. 
The mission is to apply basic concept on Data Mining and Machine Learning to develop a simple search, classification, and recommendation system. <br />



The whole web application consists of 3 features *search, classification, and recommendation* on a dataset of Ted-Talks videos from beginning to September 2017. <br />
All there features are developed inside **ted_engine.py** file, which is initialized and used by **ted.py** file. This file is a *flask* application, that connects the logic from back-end to the front-end. All files inside folder static and templates are for the *front-end HTML and CSS*  file.<br />

To replication and got the application up running in localhost, there are just some simple steps next to be done.<br />
After retrieving the project to a local machine <br />

**Step 1:**  Prepare the run environment:<br />

Because the application is written using python 3.7.0 with few necessary libraries. <br />
Make sure local machine have already installed python 3, flask, numpy, pandas, and nltk libraries. <br />
If not you can easily install python 3 and pip tool to install the needed libraries (https://realpython.com/installing-python/).<br />

**Step 2:** Execute the application:<br />

Before run, make sure you change the app.run value from host="0.0.0.0", port="80" to nothing as default. The host and port are only for when you run the application on a host.<br />
Simply run the command inside your terminal: python ted.py <br />
Your application should be up running at http://localhost:5000 <br />
You can use your browser to go to this address and start using the application. <br />
There is a search field for finding your favorite Ted-talks. There is also a recommend button under each result's videos. <br />
Finally, the classification feature helps you to classify any Ted-talks contents that you can think of. <br />



<u>**Reference:**</u><br />
Dataset: https://www.kaggle.com/rounakbanik/ted-talks <br />

Search feature built base on: https://nbviewer.jupyter.org/url/crystal.uta.edu/~cli/cse5334/ipythonnotebook/P1.ipynb

Text classification and Naïve Bayes (<https://nlp.stanford.edu/IR-book/pdf/13bayes.pdf>).Recommender 

System built base on: Chapter 9 Recommendation Systems, Mining of Massive Datasets by [Jure Leskovec](http://cs.stanford.edu/~jure/)**,** [Anand Rajaraman](https://twitter.com/anand_raj)**,** [Jeff Ullman](http://infolab.stanford.edu/~ullman/)