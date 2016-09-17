import json, os, urllib, re, nltk, time
from bs4 import BeautifulSoup
from urllib import parse

directory = "../data/en_es/"

results = {}
results["dictionary"] = {}
results["num_documents"] = 0
results["completed"] = []
dictionary = results["dictionary"]
num_documents = results["num_documents"]
completed = results["completed"]

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b.decode('utf-8'))

def iriToUri(iri):
    parts= parse.urlparse(iri)
    return parse.urlunparse([urlEncodeNonAscii(part.encode('utf-8')) for part in parts])

def getArticleContents(title):
    url = u'http://es.wikipedia.org/wiki/' + title
    url = iriToUri(url)
    print("    # Trying URL: ", url, "#")
    while True:
        try:
            html = urllib.request.urlopen(url).read().decode('utf8')
            break
        except urllib.error.HTTPError:
            return
        except UnicodeEncodeError:
            return
        except urllib.error.URLError:
            print("Internet disconnected. Sleeping 60 seconds.")
            time.sleep(60)
            pass
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find(id='mw-content-text').find_all('p')
    result = ""
    for p in content:
        result += (p.getText())
    return result

def processText(text):
    tokens = nltk.word_tokenize(text)
    tokens = [w.lower() for w in tokens if w.lower() and w.isalpha()]
    fdist = nltk.FreqDist(tokens)
    for word in fdist:
        try:
            dictionary[word]['occurances'] += fdist[word]
            dictionary[word]['documents'] += 1
        except KeyError:
            dictionary[word] = {}
            dictionary[word]['occurances'] = fdist[word]
            dictionary[word]['documents'] = 1

with open('palabras.json', 'r') as f:
    try:
        results = json.load(f)
        dictionary = results["dictionary"]
        num_documents = results["num_documents"]
        completed = results["completed"]
    except:
        pass

print("Already completed: ", completed)

for filename in os.listdir(directory):
    if filename.endswith(".json") and filename not in completed:
        path = directory + filename
        with open(path) as article_file:
            articles = json.load(article_file) 
            for en in articles:
                title = articles[en]
                title = title.replace("\\'", "'")
                contents = getArticleContents(title)
                if contents:
                    print("   ## Contents found: ", title, "##")
                    processText(contents)
                    print("   ## Text Processed: ", title, "##")
                    num_documents += 1
                    print("  ### Article complete: ", title, "###")
        print(" #### File complete: ", filename, "####")
        completed.append(filename)

    # Write our newest results to the file and continue.
    with open('palabras.json', 'w') as f:
        json.dump(results, f)
        print("##### Dumping to json #####")

