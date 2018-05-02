from nltk.tokenize import *
from nltk.corpus import stopwords
import os
import json
import sys

# define word frequency to get a cutoff
word_rep_freq=13

# Docs Source Directory
docsDirec = 'E:\coding_challneges\EigenTechnologies\Eigen_docs'
# Stop List
stoplistfile = 'stoplist.txt'
ext = '.txt'
wordDocDict={}
wordSentDict={}
finalDict={}


def print_dictionary(obj, ident):
    if type(obj) == dict:
        for k, v in obj.items():
            sys.stdout.write(ident)
            if hasattr(v, '__iter__'):
                print (k)
                print_dictionary(v, ident + '  ')
            else:
                print ('%s : %s',k, v)
    elif type(obj) == list:
        for v in obj:
            sys.stdout.write(ident)
            if hasattr(v, '__iter__'):
                print_dictionary(v, ident + '  ')
            else:
                print (v)
    else:
        print (obj)

def stopwordsGen():
    stop_words = set(stopwords.words('english'))
    uwords = set(open(stoplistfile).read().split())
    stop_words.update(uwords)
    return stop_words

def docParser(filepath):
    document_text = open(filepath,'r',encoding="utf8")
    text_string = document_text.read().lower()
    return text_string

def freqGenerator(filepath,fname):
    frequency = {}
    match_pattern = []
    text_string=docParser(filepath)
    stop_words=stopwordsGen()
    tokenizer = RegexpTokenizer(r'\w+')
    sent_list = sent_tokenize(text_string)
    for each in sent_list:
        words = tokenizer.tokenize(each)
        for w in words:
            if w not in stop_words:
                match_pattern.append(w)
    for word in match_pattern:
        count = frequency.get(word, 0)
        frequency[word] = count + 1
        wordDocDict.setdefault(word, []).append(fname)
    #Comment the below line if you dont have any limit on the frewquncy fo repetetion
    # word Frew > certain value
    p1 = {key: value for key, value in frequency.items() if value > word_rep_freq}
    # Word Freq equal to a certain value
    #p1 = {key: value for key, value in frequency.items() if value == word_rep_freq}
    s = [(k, p1[k]) for k in sorted(p1, key=frequency.get, reverse=True)]
    for key, value in s:
        for each in sent_list:
            if key in each:
                wordSentDict.setdefault(word, []).append(each)

def docWalker():
    file_dict = {}
    txt_files = [i for i in os.listdir(docsDirec) if os.path.splitext(i)[1] == ext]
    for f in txt_files:
        file_dict[f] = os.path.join(docsDirec, f)
    for fname in file_dict:
        freqGenerator(file_dict[fname],fname)

def outputProcessor():
    docWalker()
    for each in wordDocDict:
        l1=wordDocDict[each]
        d1=set(l1)
        wordDocDict[each]=list(d1)
    for each in wordSentDict:
        d={}
        d['Docs']=wordDocDict[each]
        d['Sent'] =wordSentDict[each]
        finalDict[each]=d



def writeJsonFile():
    with open('data.json', 'w') as outfile:
        json.dump(finalDict, outfile)


outputProcessor()
writeJsonFile()
print_dictionary(finalDict," ")


