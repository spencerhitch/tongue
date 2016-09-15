from flask import Flask, render_template, request
import nltk, urllib, json, string, re
from urllib import parse as urlparse
from nltk import word_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/addArticle', methods=['POST'])
def addArticle():
  title = (request.form['title'])
  url = u'http://es.wikipedia.org/wiki/' + title
  print("URL: ", url)
  url = iriToUri(url)
  html = urllib.request.urlopen(url).read().decode('utf8')
  soup = BeautifulSoup(html, "html.parser")
  content = soup.find(id='mw-content-text').find_all('p')
  result = ""
  for p in content:
      result += (p.getText())
  return result

@app.route('/generate', methods=['POST'])
def generate():
  articles = json.loads(request.form['articles'])
  text = ""
  for article in articles:
      text += articles[article]
  tokens = word_tokenize(text)
  tokens = [w.lower() for w in tokens if w.lower() not in stopwords.words('spanish') and w.isalpha()]
  fdist = nltk.FreqDist(tokens)
  common = fdist.most_common(50)
  return str(common)


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b.decode('utf-8'))

def iriToUri(iri):
    parts= urlparse.urlparse(iri)
    return urlparse.urlunparse([urlEncodeNonAscii(part.encode('utf-8')) for part in parts])
