import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import sqlite3
conn = sqlite3.connect(r"/home/manas/Documents/projects/collegeproject/data.db")
cur = conn.cursor()

headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

df = {'Projects':[],'Link':[],'Language':[],'Name':[]}

inputurl='https://github.com/adeen-s'
url=inputurl+'?tab=repositories'
content = urllib.request.urlopen(url).read()
soup = bs(content,'html.parser')

body=soup.find('div',attrs={'id':'user-repositories-list'})
#NAME
nm=soup.find('span', attrs={'class':'p-name vcard-fullname d-block overflow-hidden'})
#PROJECT
for tag in body.find_all('a',attrs={'itemprop':'name codeRepository'}):
	print(tag.text)

#LINK
for link in body.find_all('a',attrs={'itemprop':'name codeRepository'}):
	print('https://github.com'+str(link.get('href')))
	
#LANGUAGE
for div in body.find_all('div', attrs={'class':'col-10 col-lg-9 d-inline-block'}):
	x=div.find('span',attrs={'itemprop':'programmingLanguage'})
	if x is None:
		print('None')
	else:
		print(x.text)


conn.commit()
conn.close()
'''
		df['Projects'].append(tag.text)
		print(tag.text)
for link in soup.find_all('a',attrs={'itemprop':'name codeRepository'}):
		
		print(link.get('href'))
		df['Link'].append('https://github.com'+str(link.get('href')))

nm=soup.find('span', attrs={'class':'p-name vcard-fullname d-block overflow-hidden'} )
name=nm.text

for div in soup.find_all('div', attrs={'class':'col-10 col-lg-9 d-inline-block'}):
	x=div.find('span',attrs={'itemprop':'programmingLanguage'})
	if x is None:
		df['Language'].append('None')
		df['Name'].append(name)
	else:
		df['Language'].append(x.text)
		df['Name'].append(name)


print(df)
df1=pd.DataFrame(df)
print(df1)'''