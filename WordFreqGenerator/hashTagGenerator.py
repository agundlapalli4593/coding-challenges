from nltk.tokenize import *
from nltk.corpus import stopwords
import csv

stop_words = set(stopwords.words('english'))
#print(stop_words)
#print(len(stop_words))
#stopwrds_file=set(line.strip() for line in open('stoplist.txt'))
words =  set(open('stoplist.txt').read().split())
print("count from txt file",len(words))
'''stop_words.add("'ve")
stop_words.add("'s")
stop_words.add("I")
stop_words.add("us")
stop_words.add("today")
stop_words.add("That")
stop_words.add("let")
stop_words.add("It")
stop_words.add("And")
stop_words.add("thank")'''
#stop_words.union(stopwrds_file)
print("Before update",len(stop_words))
stop_words.update(words)
print("After update",len(stop_words))
word_rep_freq=2
tokenizer = RegexpTokenizer(r'\w+')
frequency = {}
match_pattern = []
document_text = open('E:\coding challneges\EigenTechnologies\Eigen_docs\doc1.txt', 'r')
text_string = document_text.read().lower()
sent_list=sent_tokenize(text_string)
for each in sent_list:
    words = tokenizer.tokenize(each)
    #words = each.split()
    #print(words)
    for w in words:
       #print(w)
       if w not in stop_words:
           print(w," Word not in stopword")
           match_pattern.append(w)
       else:
           print(w, "stopword")

for word in match_pattern:
    count = frequency.get(word, 0)
    frequency[word] = count + 1

#Filter based on the freq value.
p1=frequency
p1 = { key:value for key, value in frequency.items() if value > word_rep_freq}
s = [(k, p1[k]) for k in sorted(p1, key=frequency.get, reverse=True)]
opdict={}
for key, value in s:
    listsent = []
    for each in sent_list:
        if key in each:
            listsent.append(each)
    opdict[key]=listsent
print('word Sent')
for name, age in opdict.items():
    print('{} {}'.format(name, age))