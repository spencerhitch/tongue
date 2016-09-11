from flask import Flask, render_template, request
import nltk, urllib
from nltk import word_tokenize

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/addArticle', methods=['POST'])
def addArticle():
  title = (request.form['title'])
  print(title)
  return "OK"

