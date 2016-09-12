import numpy as np
import pandas as pd
import nltk
import jieba

#%%
def cutSentence(comment):
    
    return list(jieba.cut(comment))

def wordSet(comment):
    
    return set(cutSentence(comment))

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
all_words = set()
for item in data:
    all_words = all_words | wordSet(item[0])

all_words -= set([':', '+', 'of', 'Leonard', '"', 'exm', 'X'])

word_features = list(all_words)[:3000]
#%%
featuresets = [(generateFeature(comment), sentiment) for (comment,sentiment) in data]

train_set, test_set = featuresets[500:], featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)


#%%
print( nltk.classify.accuracy(classifier, test_set) )
#%%
classifier.show_most_informative_features(50)
