# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 14:36:31 2016

@author: zhaphotons
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:35:45 2016

@author: zhaphotons
"""

import numpy as np
import pandas as pd

import nltk
import jieba

from sklearn.naive_bayes import BernoulliNB, MultinomialNB
#%%
def cutSentence(comment):
    
    return list(jieba.cut(comment))

def wordSet(comment):
    
    return set(cutSentence(comment))

def allWordFreq(data):

    cutSencente_l = []    
    
    for item in data:
        cutSencente_l += cutSentence(item[0])
    
    return nltk.FreqDist(cutSencente_l)

def generateFeature(comment, word_features):
    
    comment_words = wordSet(comment)
    features = np.zeros(len(word_features))
    
    for i,word in enumerate(word_features):
        if word in comment_words:        
            features[i] = 1

    return features
    
def goodRatio(data):
    tot = len(data)
    count = 0
    for item in data:
        if item[1]=='Good':
            count += 1
    return count*1.0/tot

#%%
#Data
MovieName = 'Star_Trek_Beyong'
rawData = pd.read_csv(MovieName+'/'+'tmp.csv')
rawData = np.array(rawData[rawData.rating!='None'])

data = []
for item in rawData:
    comment = item[0]
    rating = int(item[1])
    
    if rating>=4:
        sentiment = 'Good'       
    else:
        sentiment = 'Bad'
    
    data.append((comment, sentiment))
    
np.random.shuffle(data)

#%%
all_words_freq = allWordFreq(data)

word_features = [item[0] for item in all_words_freq.most_common(3000)[5:]]

#%%
X = np.array([generateFeature(comment, word_features) for (comment,sentiment) in data])
y = [sentiment for (comment, sentiment) in data]

testNum = 1000
X_train, X_test = X[testNum:], X[:testNum]
y_train, y_test = y[testNum:], y[:testNum]

clf = MultinomialNB()
clf2 = BernoulliNB()
#clf.fit(X_train, y_train)

#%%
for alpha in np.linspace(0.1, 5, 20):
    clf.set_params(alpha=alpha)
    clf2.set_params(alpha=alpha)
    
    clf.fit(X_train, y_train)
    clf2.fit(X_train, y_train)

    print alpha, clf.score(X_test, y_test), clf2.score(X_test, y_test)