import sqlite3
import sys

page_items = {}
es_items = {}
result = {}

decoded = ""

with open("../data/enwiki-20160801-page.sql", 'rb') as page_db:
    for line in page_db:
        decoded = decoded + line.decode('iso-8859-1')
    for w in decoded.split("),("):
        w_split = w.split(',')
        if len(w_split) >= 3:
            page_items[w_split[0]] = w_split[2]

print(list(page_items)[0:100])

with open("../data/enwiki-20160801-langlinks.sql", 'rb') as lang_db:
    lang_db = lang_db.read().decode('iso-8859-1')
    for w in lang_db.split("),("):
        if "'es'" in w and "Categor" not in w:
            w_split = w.split(',')
            if len(w_split) >= 3:
                es_items[w_split[0]] = w_split[2]

print(list(es_items)[0:100])

for key in es_items.keys():
    try:
        result[[page_items[key]] =  es_items[key]
    except:
        continue

print(result)


