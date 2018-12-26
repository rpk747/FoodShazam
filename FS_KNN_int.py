import csv
import string
import re
import numpy as np
import pickle
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

userpref = 'Main Dishes'
itemName = []

# Cleaning the text sentences so that punctuation marks, stop words & digits are removed
def clean(doc):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    processed = re.sub(r"\d+", "", normalized)
    y = processed.split()
    return y

def loadDataset(trainingSet=[]):
    dataset = []
    global userpref

    with open('D:\Project\Multimodal\ingredients_KNN_final.csv') as csvfile:
        lines = csv.reader(csvfile)
        for row in lines:
            if row[0] == userpref:
                dataset.append(row[4])
                itemName.append(row[2])

        for data in dataset:
            cleaned = clean(data.__str__())
            #print("cleaned: " ,cleaned)
            cleaned = ' '.join(cleaned)
            cleaned = re.sub("\d+", "", cleaned.__str__())
            trainingSet.append(cleaned)

def main():
    # prepare data
    trainingSet = []
    testSet = []
    global userpref
    loadDataset(trainingSet)

    countTrainSet = (len(trainingSet))
    print('TrainSet count: ', countTrainSet)
    test = ['tomato', 'ginger', 'garlic', 'flour', 'onion', 'oil','chicken']
    #test = ['coconut milk', 'sugar', 'mangos']

    testSet_cleaned = clean(test.__str__())
    testSet_cleaned = ' '.join(testSet_cleaned)
    testSet_cleaned = re.sub(r"\d+", "", testSet_cleaned.__str__())
    testSet.append(testSet_cleaned)
    print("testSet: ",testSet)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit_transform(trainingSet)

    if userpref == 'Main Dishes':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_MainDishes.sav', 'rb'))
    elif userpref == 'Appetizers':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_Appetizers.sav', 'rb'))
    elif userpref == 'Desserts':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_Desserts.sav', 'rb'))
    Testsample = vectorizer.transform(testSet)
    print("Testsample", Testsample)

    pred = loaded_model.predict(Testsample)
    print(np.int(pred))
    print(trainingSet[np.int(pred)])
    print(itemName[np.int(pred)])

if __name__ == '__main__':
    try:
        print("hello")
        main()
    except KeyboardInterrupt:
        exit()