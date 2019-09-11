from flask import Flask, render_template, request 
from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request
import os
import sqlite3

'''project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "projectdatabase.db"))'''


app = Flask(__name__)

@app.route('/') # default route
def new():
	result = ""
	return render_template('index.html', result = result) # renders template: index.html with argument result = ""

@app.route('/result', methods = ['POST', 'GET']) # /result route, allowed request methods; POST, and GET
def predict():
	conn = sqlite3.connect(r"C:\Users\manas16b\Desktop\COLLEGE PROJECT\example1.db")
	if request.method == 'POST': 
		result = request.form["URL"]
		
		

		df = {'Projects':[],'Link':[],'Language':[],'Name':[]}

		inputurl=result
		url=inputurl+'?tab=repositories'
		content = urllib.request.urlopen(url).read()
		soup = bs(content,'html.parser')

		for tag in soup.find_all('a',attrs={'itemprop':'name codeRepository'}):
			df['Projects'].append(tag.text)
				
		for link in soup.find_all('a',attrs={'itemprop':'name codeRepository'}):
			df['Link'].append('https://github.com'+str(link.get('href')))
		nm=soup.find('span', attrs={'class':'p-name vcard-fullname d-block overflow-hidden'})
		name=nm.text

		for div in soup.find_all('div', attrs={'class':'col-10 col-lg-9 d-inline-block'}):
			x=div.find('span',attrs={'itemprop':'programmingLanguage'})
			if x is None:
				df['Language'].append('None')
				df['Name'].append(name)
			else:
				df['Language'].append(x.text)
				df['Name'].append(name)
	   
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
		

if __name__ == '__main__':
	app.debug = True
	app.run()