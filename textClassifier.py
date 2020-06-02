import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.model_selection import train_test_split # function for splitting data to train and test sets

import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
from infoStore import *
stopset = list(set(stopwords.words('english')))


def word_feats(words):
    return dict([(word, True) for word in words.split() if word not in stopset])


def listToString(s):  
	str = ""    
	for ele in s:  
		str += ele
		str += " "
    
	return str

def falseWordsPresent(link):
	words = []
	with open('E:/Project/Backend/TxtFiles/invalidWords.txt','r') as f:
		for line in f:
			for word in line.split():
				#print word
				words.append(word)	

	for word in words:
		if word in link.child or word in link.text:
			return True

	return False

def validityCheck(link):
	if falseWordsPresent(link) == True:
		return False
	url = link.child;
	text = link.text;
	breakURL = re.sub('[^A-Za-z]+',' ',url);		#it is string
	breakURL = breakURL.split(" ");					#it is list
	validityLink = classifier.classify(word_feats(listToString(breakURL))) == "positive";
	breakText = re.sub('[^A-Za-z]+',' ',text);
	breakText = breakText.split(" ");
	#print breakText;
	validityText = classifier.classify(word_feats(listToString(breakText))) == "positive";
	return (validityLink | validityText);


data = pd.read_excel('E:/Project/Backend/TxtFiles/test.csv')
data = data.sample(frac=1)
X = []
# Xa = dict()
# Xb = dict()

pos_feats = [(word_feats(str(data['text'][r])), 'positive') for r in data.index if data['value'][r] == 1] 
neg_feats = [(word_feats(str(data['text'][r])), 'negative') for r in data.index if data['value'][r] == 0] 

# print pos_feats
# for r in data.index:
# 	if data['value'][r] == 1:
# 		Xb[data['text'][r]] = True
# 	else:
# 		Xa[data['text'][r]] = True

all_feats = pos_feats + neg_feats
classifier = nltk.NaiveBayesClassifier.train(all_feats)