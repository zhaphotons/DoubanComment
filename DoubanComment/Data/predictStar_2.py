# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:35:45 2016

@author: zhaphotons
"""

import numpy as np
import pandas as pd
import nltk
import jieba

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

def generateFeature(comment):
    
    comment_words = wordSet(comment)
    features = {}
    
    for word in word_features:
        features['contains(%s)' % word] = (word in comment_words)
    
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
MovieName = 'JiShengShou.csv'
rawData = pd.read_csv(MovieName)
rawData.comment = rawData.comment.apply(str)
rawData.rating = rawData.rating.apply(str)
rawData = np.array(rawData[rawData.rating!='None'])

data = []
for item in rawData[:8000]:
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
featuresets = [(generateFeature(comment), sentiment) for (comment,sentiment) in data]

train_set, test_set = featuresets[1000:], featuresets[:1000]

classifier = nltk.NaiveBayesClassifier.train(train_set)


#%%
print( nltk.classify.accuracy(classifier, train_set) )
#%%
classifier.show_most_informative_features(50)
