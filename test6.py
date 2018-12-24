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
import itertools
from collections import defaultdict
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Cleaning the text sentences so that punctuation marks, stop words & digits are removed


def Convert(string):
    li = list(string.split(","))
    return li

train_clean_sentences = []


def clean(doc):
    stop = set(stopwords.words('english'))
    #exclude = set(string.punctuation)
    #exclude = {'.', ']', '{', "'", '-', '=', '}', '$', ':', '~', ')', ';', '<', '|', '+', '(', '%', '`', '>', '*', '#', '!', '?', '^', '[', '"', '@', '\\', '/', '&', ',', '_'}

    exclude = {'.', ']', '{',"'", '-', '=', '}', '$', ':', '~', ')', ';', '<', '|', '+', '(', '%', '`', '>', '*', '#', '!', '?', '^', '[', '"', '@', '\\', '/', '&', '_'}
    #print("exclude: ", exclude)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    #print("stop_free: ", stop_free)
    #print("stop_free next: ", re.sub("[\"[].*?[\]"]", "[\(].*?[\)]", stop_free))
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    #print("punc_free: ",punc_free)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    #print("normalized: ",normalized)
    processed = re.sub(r"\d+", "", normalized)
    #print("processed: ", processed)
    #print("processed1: ", re.sub("[\,]", "", processed))

    processed = Convert(processed)
    #print("processed2: ", processed)
    processed = [x.strip(' ') for x in processed]
    #print("processed2new: ", processed)
    #y = processed.split()
    #print("y: ", y)

    return processed

all_ingredients_text = []
def loadDataset(trainingSet=[]):
    with open('D:\Project\Multimodal\ingredients_v4_5000.csv', 'r') as csvfile:
        lines = csv.reader(csvfile)
        # print(lines)
        dataset = list(lines)
        print("dataset :", dataset)

        for data in dataset:
            print("data:", data)
            cleaned = re.sub("[\(].*?[\)]", "", data.__str__())
            #print("cleaned1: ", cleaned)
            #cleaned = re.sub("[\,].*?[\']", ",'", cleaned.__str__())
            cleaned = re.sub("(Teaspoon|teaspoon|Tablespoon|tablespoon|lb|tsp|cups|cup|tb|Tbs|Oz|OZ|minced|bruised|pinch|freshly|chopped)", "", cleaned.__str__())
            #print("cleaned2: ", cleaned)
            cleaned = clean(cleaned.__str__())
            #print("cleaned3: ", cleaned)
            for ing in cleaned:
                all_ingredients_text.append(ing)
            # cleaned = ' '.join(cleaned)
            cleaned = re.sub("\d+", "", cleaned.__str__())
            # print("cleanedjoin: ", cleaned)
            trainingSet.append(cleaned)
            train_clean_sentences.append(cleaned)

        print("trainingSet :", trainingSet)


def to_ingredient(text):
    "Transforms text into an ingredient."
    return frozenset(re.split(re.compile('[,. ]+'), text))


def candidates(ingredient):
    "Returns a list of candidate ingredients obtained from the original ingredient by keeping at least one of them."
    n = len(ingredient)
    possible = []
    for i in range(1, n + 1):
        possible += [frozenset(combi) for combi in itertools.combinations(ingredient, i)]
    return possible

def candidates_increasing_distance(ingredient, vocabulary):
    "Returns candidate ingredients obtained from the original ingredient by substraction, largest number of ingredients first."
    n = len(ingredient)
    for i in range(n - 1, 1, -1):
        possible = [frozenset(combi) for combi in itertools.combinations(ingredient, i)
                    if frozenset(combi) in vocabulary]
        if len(possible) > 0:
            return possible
    return [ingredient]

def best_replacement(ingredient, probability):
    "Computes best replacement ingredient for a given input."
    return max(candidates(ingredient), key=lambda c: probability[c])

def best_replacement_increasing_distance(ingredient, vocabulary):
    "Computes best replacement ingredient for a given input."
    return max(candidates_increasing_distance(ingredient, vocabulary), key=lambda w: vocabulary[w])

def main():
    # prepare data
    trainingSet = []
    testSet = []
    loadDataset(trainingSet)
    print("trainingSet :", trainingSet)
    print("all_ingredients_text :", all_ingredients_text)

    all_ingredients_textnew = (list(filter(None, all_ingredients_text))).copy()
    print("all_ingredients_textnew :", all_ingredients_textnew)
    all_ingredients = []
    for text in all_ingredients_textnew:
            all_ingredients.append(to_ingredient(text))
    print("all_ingredients: ", all_ingredients)

    c = Counter(all_ingredients)
    #print("c: ", c.most_common(20))

    probability = defaultdict(lambda: 1, c.most_common())
    #print("probability: ", probability[to_ingredient('black pepper powder')])
    #print("candidates :", candidates(to_ingredient("pinch freshly ground white pepper")))
    #print("replacement :", best_replacement(to_ingredient("fresh frozen veggie choice"),probability))

    vocabulary = dict(c.most_common())
    #print("replacement :", best_replacement_increasing_distance(to_ingredient('water'), vocabulary))
    cleanedSet = []
    ingredientListnew = []
    exclude = {'[',']',"'"}
    for ingredientlist in trainingSet:
        print("ingredient : ",ingredientlist)
        ingredientlist = Convert(ingredientlist)
        #ingredientlist = (list(filter(None, ingredientlist))).copy()
        #print("ingredient : ", ingredientlist)
        for ing in ingredientlist:
            #print("ing : ", ing)
            #print("ing : ", ''.join(ch for ch in ing if ch not in exclude))
            ingnew = ''.join(ch for ch in ing if ch not in exclude)
            print("ingnew : ", ingnew.strip(' '))
            print("ingnew1 : ", ''.__len__())

            if ingnew.__len__() != 1 and ingnew.__len__() != 0:
                ingreplacement = best_replacement_increasing_distance(to_ingredient(ingnew.strip(' ')), vocabulary)
                print("ingreplacement : ", ingreplacement)
                ingreplacement2 = best_replacement(to_ingredient(ingnew.strip(' ')), probability)
                print("ingreplacement2 : ", ingreplacement2)
            ingredientListnew.append((" ".join(ingreplacement)))
        cleanedSet.append(ingredientListnew.copy())
        ingredientListnew.clear()

        print("cleanedSet : ", cleanedSet)
        myFile = open('D:\Project\Multimodal\ingredients_23.csv', 'w')
        with myFile:
            writer = csv.writer(myFile)
            writer.writerows(cleanedSet)

if __name__ == '__main__':
    try:
        print("hello")
        main()
    except KeyboardInterrupt:
        exit()
