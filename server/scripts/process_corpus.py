import nltk, json
from nltk.corpus import cess_esp as es
fd = nltk.FreqDist(es.words())
fd = fd.most_common()
result = {}

print(len(fd))

for w in fd:
    result[w[0]] = w[1]

with open('../data/es_freq_anal.json', 'w') as outfile:
    json.dump(result, outfile)


