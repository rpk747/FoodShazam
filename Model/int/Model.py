import csv
import string
import re
import numpy as np
import pickle
import pandas as pd
import requests
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

userpref = None
itemName = []
recipeID = []
orgIngredients=[]
# store API access key
cykey = '_app_id=f2a8aed2&_app_key=2e1518e4407a359e7db7b496841bc713'

# create wrapper function
def recipeOutputter(cuis):
    result = []
    r = (requests.get('http://api.yummly.com/v1/api/recipes?_app_id=f2a8aed2&_app_key=2e1518e4407a359e7db7b496841bc713&q='+itemName[cuis])).json()
    #print(r)
    recipes = pd.DataFrame(r['matches'], columns=[ 'id', 'smallImageUrls', 'recipeName','ingredients'])
    #print(recipes)
    # extract course and cusine and add to DF
    itemID = []
    itemRecipeName = []
    itemIngredients = []
    for i in r['matches']:
        itemID.append(i['id'])
        itemRecipeName.append(i['recipeName'])
        itemIngredients.append(i['ingredients'])

    result.append(recipeID[cuis])
    result.append(itemName[cuis])
    result.append(orgIngredients[cuis])
    #img_data = requests.get('https://lh3.googleusercontent.com/fXEuO9p7Uf6n4JhUqNMQGwHg8-s2y885t1DDYTpYp9_7yIX_Vqquwzl9QJxPJXZ_RE9Zlded1Negn2V-2wLWog=s90').content
    #with open('C:/Users/Rohit/PycharmProjects/FSS_int_scrapping/'+itemRecipeName[0]+'.jpg', 'wb') as handler:
        #handler.write(img_data)

    return result
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
                recipeID.append(row[5])
                orgIngredients.append(row[3])

        for data in dataset:
            cleaned = clean(data.__str__())
            #print("cleaned: " ,cleaned)
            cleaned = ' '.join(cleaned)
            cleaned = re.sub("\d+", "", cleaned.__str__())
            trainingSet.append(cleaned)

def FS_model(pref,ingSet=[]):
    # prepare data
    #print("pref: ",pref)
    #print("ingSet: ", ingSet)
    global userpref
    userpref = pref
    trainingSet = []
    testSet = []
    loadDataset(trainingSet)
    testSet_cleaned = clean(ingSet.__str__())
    testSet_cleaned = ' '.join(testSet_cleaned)
    testSet_cleaned = re.sub(r"\d+", "", testSet_cleaned.__str__())
    testSet.append(testSet_cleaned)
    #print("testSet: ",testSet)

    vectorizer = TfidfVectorizer(stop_words='english')
    vectorizer.fit_transform(trainingSet)

    if userpref == 'Main Dishes':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_MainDishes.sav', 'rb'))
    elif userpref == 'Appetizers':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_Appetizers.sav', 'rb'))
    elif userpref == 'Desserts':
        loaded_model = pickle.load(open('D:\Project\Multimodal\ingredients_Desserts.sav', 'rb'))
    Testsample = vectorizer.transform(testSet)
    #print("Testsample", Testsample)

    pred = loaded_model.predict(Testsample)
    #print(np.int(pred))
    #print(trainingSet[np.int(pred)])
    #print(itemName[np.int(pred)])
    result = recipeOutputter(np.int(pred))
    return result