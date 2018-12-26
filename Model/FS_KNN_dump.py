import csv
import random
import math
import operator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle

# Cleaning the text sentences so that punctuation marks, stop words & digits are removed
def clean(doc):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    #print("stop_free: ",stop_free)
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #print("punc_free: ",punc_free)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    #print("normalized: ",normalized)
    processed = re.sub(r"\d+", "", normalized)
    y = processed.split()
    #print(y)
    return y
train_clean_sentences = []

dataset = []
userpref = 'Appetizers'
def loadDataset(trainingSet=[]):
    global userpref
    with open('D:\Project\Multimodal\ingredients_KNN_final.csv') as csvfile:
        lines = csv.reader(csvfile)
        for row in lines:
            #print(row[0])
            if row[0] == userpref:
                dataset.append(row[4])

        #print("dataset :" ,dataset)
        for data in dataset:
            cleaned = clean(data.__str__())
            #print("cleaned: " ,cleaned)
            cleaned = ' '.join(cleaned)
            cleaned = re.sub("\d+", "", cleaned.__str__())
            trainingSet.append([cleaned])
            train_clean_sentences.append(cleaned)

        #print("trainingSet :", trainingSet)

def main():
    # prepare data
    trainingSet = []
    testSet = []

    loadDataset(trainingSet)
    global userpref
    countTrainSet = (len(trainingSet))
    print('Train: ', countTrainSet)
    #print(trainingSet)
    test = ['tomato', 'ginger', 'garlic', 'flour', 'onion', 'oil','chicken']
    #test = ['coconut milk', 'sugar', 'mangos']

    testSet_cleaned = clean(test.__str__())
    testSet_cleaned = ' '.join(testSet_cleaned)
    testSet_cleaned = re.sub(r"\d+", "", testSet_cleaned.__str__())
    testSet.append(testSet_cleaned)
    print("testSet: ",testSet)
    #print("train_clean_sentences: ", train_clean_sentences)
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(train_clean_sentences)

    #print("vectorizer:", vectorizer.get_feature_names())
    #print("X:", X.shape)

    #y_train = np.zeros(countTrainSet)
    #y_train[1:countTrainSet] = np.arange(1,countTrainSet,1)
    #print("y_train",y_train)
    #modelknn = KNeighborsClassifier(n_neighbors=1)
    #modelknn.fit(X, y_train)
    #pickle.dump(modelknn, open('D:\Project\Multimodal\ingredients_Desserts.sav', 'wb'))

    if userpref == 'MainDishes':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_MainDishes.sav', 'rb'))
    elif userpref == 'Appetizers':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_Appetizers.sav', 'rb'))
    elif userpref == 'Desserts':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_Desserts.sav', 'rb'))
    Testsample = vectorizer.transform(testSet)
    print("Testsample", Testsample)

    #print(np.int(modelknn.predict(Testsample[0])))
    #print(train_clean_sentences[np.int(modelknn.predict(Testsample[0]))])

    pred = loaded_model.predict(Testsample)
    print(np.int(pred))
    print(train_clean_sentences[np.int(pred)])

if __name__ == '__main__':
    try:
        print("hello")
        main()
    except KeyboardInterrupt:
        exit()