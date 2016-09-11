from flask import Flask, render_template, request
import nltk, urllib
from nltk import word_tokenize
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/addArticle', methods=['POST'])
def addArticle():
  title = (request.form['title'])
  url = 'http://en.wikipedia.org/wiki/' + title
  html = urllib.request.urlopen(url).read().decode('utf8')
  soup = BeautifulSoup(html)
  content = soup.find(id='mw-content-text').find_all('p')
  for p in content:
      print(p.getText())
  return "OK"

