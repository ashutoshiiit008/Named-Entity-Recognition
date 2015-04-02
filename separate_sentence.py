import re
import json, requests, ast ,re
from sentimentanalysis import  cleaner, sentiment
import sentimentanalysis.FullNNP as fullname
from collections import Counter
from city_name_dict import *
from location_dictionary import *
from and_condition import *
import urllib
import urllib2
import time as tag 
import time as extract 
import sys
from stanford import client101
from nltk.stem.wordnet import WordNetLemmatizer

#coding: utf8 
import os



import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import stem
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk import stem
from bs4 import UnicodeDammit
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def super_clean(text):
	dammit = UnicodeDammit(text)
	cdata = dammit.unicode_markup
	cdata = cdata.encode('utf-8')
	return cdata

para = open ('news.txt' , 'r').read().strip()
def split_into_sentences(text):
    pattern = "\.[A-Z]"
    # print text
    regex = re.findall(pattern, text, flags=0)
    regex = list(set(regex))
    if regex:
        for ele in regex:
            text = text.replace(ele,'. ' + ele[-1])
    text = text.decode('utf-8').encode('ascii', 'ignore')
    sents = sent_tokenizer.tokenize(text)
    return sents

para =  super_clean(para)
split_sent = split_into_sentences(para)
for each in split_sent:
    print each 
    
