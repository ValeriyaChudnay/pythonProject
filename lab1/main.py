import csv
import operator
import matplotlib.pylab as plt

from nltk import collections, PorterStemmer

with open('lab1/stop-words.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    stopWord = list(reader)

def isStopWord(word):
    for sWord in stopWord[0]:
        if sWord == word:
            return True
    return False

def convertStringToList(string):
    li = list(string.split(" "))
    res=[]
    for l in li:
        l=l.lower()
        if not isStopWord(l) and len(l)>0:
            res=res+[l]
    return res



with open('lab1/sms-spam-corpus.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    porter = PorterStemmer()
    spam = []
    spamMap = {}
    hum=[]
    specialSymbol = ",.1234567890?`-=\]'><[;/!@#$%^&*()_+|}{|:'\""
    for row in spamreader:
        if row[0] == "spam":
            for word in row:
                if len(word) > 0 and word!=row[0] :
                    word=porter.stem(word)
                    word = word.translate({ord(i): None for i in specialSymbol})
                    spam=spam+convertStringToList(word)

        # else:
        #     for word in row:
        #         if len(word) > 0:
        #             word = word.translate({ord(i): None for i in specialSymbol})
        #             if (not isStopWord(word)):
        #                  print(word)
    for s in spam:
        if s in spamMap:
            spamMap.update({s:spamMap.get(s)+1})
        else:
            spamMap[s]=1
    spamMap=sorted(spamMap.items(), key=operator.itemgetter(1), reverse=True)

    print(spamMap)
    first20Spam= dict(spamMap[:20])
    print(first20Spam)
    # x, y = zip(*spamMap)  # unpack a list of pairs into two tuples
    # plt.plot(x, y)
    # plt.show()
    plt.bar(*zip(*first20Spam.items()))
    plt.show()