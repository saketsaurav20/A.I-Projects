#web scrapping with the help of beautiful soup
from bs4 import BeautifulSoup
import requests
import re
import operator
import json
from tabulate import tabulate
import sys
from stop_words import get_stop_words

#get the words
def getWordList(url):
    word_list = []

    #raw data
    source_code = requests.get(url)

    #convert to text
    plain_text = source_code.text

    #lxml format
    soup = BeautifulSoup(plain_text,'html.parser')

    #find the words in paragraph tag
    for text in soup.findAll('p'):
        if text.text is None:
            continue
        content = text.text
        #lowercase and split into an array
        words = content.lower().split()

        for word in words:
            #remove non-chars
            cleaned_word = clean_word(word)
            #if there is still something there
            if len(cleaned_word) > 0:
                #add it to our word list
                word_list.append(cleaned_word)

    return word_list

def createFrquencyTable(word_list):
    word_count = {}
    for word in word_list:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    return word_count

#clean word with regex
def clean_word(word):
    cleaned_word = re.sub('[^A-Za-z]+', '', word)
    return cleaned_word

#remove stopwords
def remove_stop_words(frequency_list):
    stop_words = get_stop_words('en')

    temp_list = []
    for key,value in frequency_list:
        if key not in stop_words:
            temp_list.append([key, value])

    return temp_list

#keyword you want to search
string_query = "batman"

#to remove stop words or not
search_mode = True
#search_mode = False

#access wiki API. json format. query it for data. search tyep. shows list of possibilities
wikipedia_api_link = "https://en.wikipedia.org/w/api.php?format=json&action=query&list=search&srsearch="
wikipedia_link = "https://en.wikipedia.org/wiki/"
url = wikipedia_api_link + string_query


#try-except block. simple way to deal with exceptions 
#great for HTTP requests
try:
    #use requests to retrieve raw data from wiki API URL we
    #just constructed
    response = requests.get(url)

    #format that data as a JSON dictionary
    data = json.loads(response.content.decode("utf-8"))

    #page title, first option
    #show this in web browser
    wikipedia_page_tag = data['query']['search'][0]['title']

    #get actual wiki page based on retrieved title
    url = wikipedia_link + wikipedia_page_tag
    #get list of words from that page
    page_word_list = getWordList(url)
    #create table of word counts, dictionary
    page_word_count = createFrquencyTable(page_word_list)
    #sort the table by the frequency count
    sorted_word_frequency_list = sorted(page_word_count.items(), key=operator.itemgetter(1), reverse=True)
    #remove stop words if the user specified
    if(search_mode):
        sorted_word_frequency_list = remove_stop_words(sorted_word_frequency_list)

    #sum the total words to calculate frequencies   
    total_words_sum = 0
    for key,value in sorted_word_frequency_list:
        total_words_sum = total_words_sum + value

    #just get the top 20 words
    if len(sorted_word_frequency_list) > 20:
        sorted_word_frequency_list = sorted_word_frequency_list[:20]

    #create our final list which contains words, frequency (word count), percentage
    final_list = []
    for key,value in sorted_word_frequency_list:
        percentage_value = float(value * 100) / total_words_sum
        final_list.append([key, value, round(percentage_value, 4)])

    #headers before the table
    print_headers = ['Word', 'Frequency', 'Frequency Percentage']

    #print the table with tabulate
    print(tabulate(final_list, headers=print_headers, tablefmt='orgtbl'))

#throw an exception in case it breaks
except requests.exceptions.Timeout:
    print("The server didn't respond. Please, try again later.")