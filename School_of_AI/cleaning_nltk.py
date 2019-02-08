## using natural language toolkit for data cleaning 
#tokenize the word
#load the word
filename='metamorphosis_clean.txt'
file=open(filename,'rt')
text=file.read()
file.close()

#split into words
from nltk.tokenize import word_tokenize
tokens=word_tokenize(text)
print(tokens[:100])

#split as a sentence
from nltk.tokenize import sent_tokenize
tokens_new=sent_tokenize(text)
print(tokens_new[:100])

#remove the word which is not alphabet
words=[word for word in tokens if word.isalpha()]
print(words[:100])

#filter out stopword and pipelines
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
print(stop_words)

