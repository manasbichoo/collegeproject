from flask import Flask, render_template, request ,url_for
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request
import os
import sqlite3
import cgitb
from flask_bootstrap import Bootstrap 


# NLP Packages
from textblob import TextBlob,Word 
import random 
import time

'''project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "projectdatabase.db"))'''


app = Flask(__name__)
Bootstrap(app)


@app.route('/feedback')
def feedback():
	return render_template('feedback.html')

@app.route('/') # default route
def new():
	result = ""
	return render_template('index.html', result = result) # renders template: index.html with argument result = ""

@app.route('/result', methods = ['POST', 'GET']) # /result route, allowed request methods; POST, and GET
def predict():
	conn = sqlite3.connect(r"/home/manas/Documents/projects/collegeproject/example2.db")
	if request.method == 'POST': 
		result = request.form["URL"]
		
		

		df = {'Projects':[],'Link':[],'Language':[],'Name':[]}

		inputurl=result
		url=inputurl+'?tab=repositories'
		content = urllib.request.urlopen(url).read()
		soup = bs(content,'html.parser')

		for tag in soup.find_all('a',attrs={'itemprop':'name codeRepository'}):
			df['Projects'].append(str(tag.text))
				
		for link in soup.find_all('a',attrs={'itemprop':'name codeRepository'}):
			df['Link'].append("https://github.com"+str(link.get('href')))
		
		nm=soup.find('span', attrs={'class':'p-name vcard-fullname d-block overflow-hidden'})
		name=nm.text

		for div in soup.find_all('div', attrs={'class':'col-10 col-lg-9 d-inline-block'}):
			x=div.find('span',attrs={'itemprop':'programmingLanguage'})
			if x is None:
				df['Language'].append('None')
				df['Name'].append(str(name))
			else:
				df['Language'].append(x.text)
				df['Name'].append(str(name))
	   
		df1=pd.DataFrame(df)
		
		#Database
		cur = conn.cursor()
		df1.to_sql('Projects', conn,if_exists='append', index=False) # - writes the pd.df to SQLIte DB
		pd.read_sql('select * from Projects', conn)
		conn.commit()
		conn.close()

		return render_template('index.html',result=url, table = df1.to_html()) # renders template: index.html with argument result = polarity value calculated
	else:
		return render_template('index.html')	



@app.route('/analyse',methods=['POST','GET'])
def analyse():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		#NLP Stuff
		blob = TextBlob(rawtext)
		received_text2 = blob
		blob_sentiment,blob_subjectivity = blob.sentiment.polarity ,blob.sentiment.subjectivity
		number_of_tokens = len(list(blob.words))
		# Extracting Main Points
		nouns = list()
		for word, tag in blob.tags:
			if tag == 'NN':
				nouns.append(word.lemmatize())
				len_of_words = len(nouns)
				rand_words = random.sample(nouns,len(nouns))
				final_word = list()
				for item in rand_words:
					word = Word(item).pluralize()
					final_word.append(word)
					summary = final_word
					end = time.time()
					final_time = end-start
		return render_template('feedback.html',received_text = received_text2,number_of_tokens=number_of_tokens,blob_sentiment=blob_sentiment,blob_subjectivity=blob_subjectivity,summary=summary,final_time=final_time)

	else:
		return render_template('feedback.html')



@app.route('/test',methods=['POST','GET'])
def test():
	if request.method == 'POST': 
		result = request.form["ac"]
		return render_template('test.html',result=result)
	else:
		return render_template('test.html')



		

if __name__ == '__main__':
	app.debug = True
	app.run()