# -*- coding: utf-8 -*-
"""
Created on Sun Sep  4 15:45:54 2016

@author: new
"""

def gender_features1(name):
    
    features = {}
    features['firstletter'] = name[0].lower()
    features['lastletter'] = name[-1].lower()
    
    return features    

def gender_features2(name):

    features = {}
    features['firstletter'] = name[0].lower()
    features['lastletter'] = name[-1].lower()
    
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        features['count(%s)' % letter] = name.lower().count(letter)
        features['has(%s)' % letter] = (letter in name.lower())
    
    
    return features

def gender_features3(name):
    
    features = {}
    features['lastletter'] = name[-1].lower()
    features['last2letter'] = name[-2:].lower()    
    features['last3letter'] = name[-3:].lower()
    features['firstletter'] = name[:1].lower()
    features['first2letter'] = name[:2].lower()
    features['first3letter'] = name[:3].lower()    
    
    return features    

    
#re = gender_features2('John')
#
#print(re)
#%%
import nltk
from nltk.corpus import  names
from nltk.classify import apply_features
import random



names = [(name, 'male') for name in names.words('male.txt')] + \
        [(name, 'female') for name in names.words('female.txt')]

random.shuffle(names)

gender_features = gender_features3

train_names = names[1500:]
devtest_names = names[500:1500]
test_names = names[:500]

train_set = apply_features(gender_features, train_names)
devtest_set = apply_features(gender_features, devtest_names)
test_set = apply_features(gender_features, test_names)

classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, devtest_set))
print(classifier.show_most_informative_features(20))


#%%
errors = []

for name, tag in test_names:
    guess = classifier.classify(gender_features(name))
    if guess != tag:
        errors.append((tag, guess, name))

for (tag, guess, name) in sorted(errors):
    print('correct:%s guess:%s name:%s' % (tag, guess, name))
