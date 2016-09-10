import sqlite3, json
import string

page_items = {}
es_items = {}
result = {}
alpha = string.ascii_lowercase

decoded = ""

# Fill results dictionary with two letter character combos
for letter0 in alpha:
    for letter1 in alpha:
        alpha_entry = letter0 + letter1
        result[alpha_entry] = {}

#Open EnglishWiki pages and get their pageids and titles
with open("../data/enwiki-20160801-page.sql", 'rb') as page_db:
    for line in page_db:
        decoded = decoded + line.decode('iso-8859-1')
    for w in decoded.split("),("):
        w_split = w.split(',')
        if len(w_split) >= 3:
            title = w_split[2].replace(" ", "_")
            page_items[w_split[0]] = title[1:len(title)-2]

# Open the language links from all EnglishWiki entries, extract the 
# spanish titles and associated english lanugae pageids
with open("../data/enwiki-20160801-langlinks.sql", 'rb') as lang_db:
    lang_db = lang_db.read().decode('iso-8859-1')
    for w in lang_db.split("),("):
        if "'es'" in w and "Categor" not in w:
            w_split = w.split(',')
            if len(w_split) >= 3:
                title = w_split[2].replace(" ", "_")
                es_items[w_split[0]] = title[1:len(title)-2]
# Because corresponding pageids, we iterate through our keys and
for key in es_items.keys():
    try:
        alpha_key = page_items[key][0:2].lower()
        result_alpha = result[alpha_key]
        result_alpha[page_items[key]] = es_items[key]
    except:
        continue

for key in result.keys():
  url = '../data/en_es/' + key + '.json'
  with open(url, 'w') as writefile:
    json.dump(result[key], writefile)


