from flask import Flask, render_template, request
import nltk, urllib, json, re, operator
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
  top = []
  spanish_words = []
  # TODO: I suppose all of this should be precomputed, stored in json then just imported
  with open('./server/data/es_freq_anal.json') as json_data:
    freq_data = json.load(json_data)
    sorted_freq = sorted(freq_data.items(), key=operator.itemgetter(1), reverse=True)
    spanish_words = [w[0] for w in sorted_freq] 
    top = spanish_words[0:15000]
  text = ""
  for article in articles:
      text += articles[article]
  tokens = word_tokenize(text)
  tokens = [w.lower() for w in tokens if w.lower() not in top
           and w.isalpha() and w.lower() in spanish_words]
  fdist = nltk.FreqDist(tokens)
  common = fdist.most_common(50)
  return json.dumps(common)


def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b.decode('utf-8'))

def iriToUri(iri):
  parts= urlparse.urlparse(iri)
  return urlparse.urlunparse([urlEncodeNonAscii(part.encode('utf-8')) 
    for part in parts])
