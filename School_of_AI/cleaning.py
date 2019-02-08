##cleaning the data manually by using python3

#load the text
filename='Metamorphosis_clean.txt'
file=open(filename, 'rt')
text=file.read()
file.close()


##split by white space
#split into words by white spaces
words=text.split()
print(words[:100])

##split by words 
#import re
#words=re.split(r"\w+",text)
#print(words[:100])

##remove punctuation from each word
#maketrans is a static method-by using z=string.punctuation it mapped all the punctuation to none and then
#we pass it to the translator to translate by omitting punctuation
import string
table=str.maketrans('','',string.punctuation)
stripped=[w.translate(table) for w in words]
print(stripped[:100])

##Capitalization
#but we need to take care of US is not converted into small letter us
words=[word.lower() for word in words]
print(words[:100])