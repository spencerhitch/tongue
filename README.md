##Description
Tongue is a webapp for intermediate language learners to build vocabulary lists relative to their interests.

##Motivation
[Zipf's Law](https://en.wikipedia.org/wiki/Zipf%27s_law) states "given some corpus of natural language utterances, the frequency of any word is inversely proportional to its rank in the frequency table." This means the 10 most popular words in a language make up 25% of the language's usage, the top 100 words make up 50%, the top 1000, 75%, and top 7000, 90%. To get to 95% (one measure of fluency), a learner must have command of 50,000 words!

Language learning software and language courses can do a good job helping a learner to master those top 1000 words. After that the pool of words between a learner and fluency becomes seemingly insurmountable. So how do we go about learning those other 20% of words in usage (49,000 words!)?

Tongue proposes that the bottom 20% of words are going to be specific to what the topics of conversation a speaker engages in. Your interests determine your vocabulary. Tongue allows language learners to build a vocabulary list to support conversation in topics they are interested in.

##How It Works
* A user builds a list of Wikipedia articles in their native language. This list enumerates a user's particular interests.
* Look at the corresponding articles in the user's target language
* Analyze the word occurances in the target language articles and compare with occurances in a general corpus for target language
* Yield a list of interesting words that occur disproportionately relative to the user's interests

###Notes
* Version 0.0.0 is built only to support English speaking Spanish learners
* get the sql dumps of English wikipedia articles, make a python pkl with:
  ```
  {English_Article_Title : Spanish_Version_Link}
  ```
* Freq anal data of spanish lang corpus
* User creates list and hits 'process'
* server-side py html.GETs every article, tokenizes, frequency analysis (freqAnal)
* compare user's freqAnal w/ freqAnal of large spanish language corpus (stored on server)

* We're generating a list of tf-idf scores for every word in spanish-language wikipedia
* We look at the set of words in the articles our user has chosen then look at the tf-idf of those words and return the highest scoring


