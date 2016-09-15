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
    start_insert = False
    insert_query = b"INSERT INTO `page` VALUES ("
    for line in page_db:
        if start_insert:
            decoded = decoded + line.decode('utf-8')
        elif line.find(insert_query) >= 0:
            start_insert = True
            decoded = decoded + line.decode('utf-8')[len(insert_query):]
        else:
            continue
    print("finished decoding")
    for w in decoded.split("),("):
        w_split = w.split(',')
        if len(w_split) >= 3:
            i = 2
            title = w_split[i]
            while not title.endswith("'"):
              i += 1
              title = title + "," + w_split[i]
            title = title.replace(" ", "_")
            title = title[1:len(title)-1]
            page_items[w_split[0]] = title

print("finished with page: ", len(page_items))

# Open the language links from all EnglishWiki entries, extract the 
# spanish titles and associated english lanugae pageids
with open("../data/enwiki-20160801-langlinks.sql", 'rb') as lang_db:
    lang_db = lang_db.read()
    for w in lang_db.split(b"),("):
        if b"'es'" in w and b"Categor" not in w and b"Usario" not in w and b"Ayuda" not in w:
            w_split = w.split(b",")
            if len(w_split) >= 3:
                i = 2
                title = w_split[i]
                while not title.endswith(b"'"):
                  i += 1
                  title = title + b"," +  w_split[i]; 
                title = w_split[2].replace(b" ", b"_")
                try:
                  title = title[1:len(title)-1].decode('utf-8')
                  page_id = w_split[0].decode('utf-8')
                  es_items[page_id] = title
                except UnicodeDecodeError:
                    continue

print("finished with lang_links: ", len(es_items))
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
