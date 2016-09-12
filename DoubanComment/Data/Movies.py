# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 20:37:07 2016

@author: new
"""

import nltk
from nltk.corpus import  movie_reviews

import random

#%%
def document_features(document):

    document_words = set(document)
    features = {}
    
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    
    return features


#%%
documents = [(list(movie_reviews.words(fileid)), category) 
              for category in movie_reviews.categories()
              for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)


#%%
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
#word_features = list(all_words.keys())[:6000]

mostWords = all_words.most_common(5000)
word_features = [item[0] for item in mostWords[20:]]


featuresets = [(document_features(d), c) for (d,c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]

classifier = nltk.NaiveBayesClassifier.train(train_set)


#%%
print( nltk.classify.accuracy(classifier, test_set) )
#%%
classifier.show_most_informative_features(20)