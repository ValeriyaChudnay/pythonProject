import csv
import math
import operator
import re

import matplotlib.pylab as plt
from nltk import PorterStemmer
from nltk.corpus import stopwords

porter = PorterStemmer()


def gathering_to_set(flist):
    res = {}
    for s in flist:
        if s in res:
            res.update({s: res.get(s) + 1})
        else:
            res[s] = 1
    return sorted(res.items(), key=operator.itemgetter(1), reverse=True)


def get_first_20(flist):
    return dict(flist[:20])


def isStopWord(word):
    if word in stopwords.words('english'):
        return True
    return False


def convertStringToListAndStem(string):
    li = list(string.split(" "))
    res = []
    for l in li:
        l = l.lower()
        l = porter.stem(l)
        if not isStopWord(l) and len(l) > 0:
            res = res + [l]
    return res


def printPlot(map,title):
    plt.title(title)
    plt.bar(*zip(*map.items()))
    plt.show()

def printPlotWithAverege(averege,map,title):
    plt.title(title)
    plt.xlabel('length')
    plt.ylabel('count')
    plt.bar(*zip(*map.items()),color = "#ff3da2")
    plt.axvline(averege, color='k', linestyle='dashed', linewidth=1)
    plt.show()


def saveToCsv(map, name):
    map = dict(map)
    with open(name, 'w') as f:
        for key in map:
            f.write("%s,%s\n" % (key, map[key]))


def deleteSpecialSymbolsFromString(string):
    string = re.sub('[^a-zA-Z \n]', ' ', string)
    return convertStringToListAndStem(string)


def cleanRow(type, string):
    if type == "spam":
        return string[4:]
    else:
        return string[3:]


def countMessageLenth(mySet, lenth):
    if lenth in mySet.keys():
        mySet.update({lenth: mySet.get(lenth) + 1})
    else:
        mySet[lenth] = 1
    return mySet

def getAverege(set):
    summa = 0
    count = 0
    for a in set:
        summa = summa + a[0] * a[1]
        count = count + a[1]
    return summa / (count * 1.0)

def normilize(set):
    summa = 0
    for a in set:
        summa = summa + a[0] * a[1]
    setN=dict(set)
    for a in setN:
        setN.update({a: setN.get(a)/summa})
    return setN

def normilizeDict(set):
    summa = 0
    for v in set:
        summa = summa + v[1]
    for i in range(len(set)):
        set[i][1]=set[i][1]/summa
    return set

def lab1Main():
    with open('lab1/sms-spam-corpus.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        wordsSpam = {}
        messageSpam = {}
        wordsHum = {}
        messageHum = {}
        spam = []
        hum = []
        for row in spamreader:
            if row[0] == "spam":
                row = cleanRow(row[0], ''.join(row))
                messageSpam = countMessageLenth(messageSpam, len(row))
                spam = spam + deleteSpecialSymbolsFromString(row)
            elif row[0] == "ham":
                row = cleanRow(row[0], ''.join(row))
                messageHum = countMessageLenth(messageHum, len(row))
                hum = hum + deleteSpecialSymbolsFromString(row)

    spamMap = normilizeDict(gathering_to_set(spam))
    humMap = normilizeDict(gathering_to_set(hum))

    # for word in spamMap:
    #     wordsSpam = countMessageLenth(wordsSpam, len(word[0]))
    # for word in humMap:
    #     wordsHum = countMessageLenth(wordsHum, len(word[0]))
    #
    # wordsSpam = sorted(wordsSpam.items(), key=operator.itemgetter(1), reverse=True)
    # wordsHum = sorted(wordsHum.items(), key=operator.itemgetter(1), reverse=True)
    # messageSpam = sorted(messageSpam.items(), key=operator.itemgetter(1), reverse=True)
    # messageHum = sorted(messageHum.items(), key=operator.itemgetter(1), reverse=True)

    # printPlot(get_first_20(spamMap), "Spam")
    # printPlot(get_first_20(humMap), "Hum")
    #
    # printPlotWithAverege(getAverege(wordsSpam), normilize(wordsSpam), "wordsSpam")
    # printPlotWithAverege(getAverege(wordsHum), normilize(wordsHum), "wordsHum")
    # printPlotWithAverege(getAverege(messageSpam), normilize(messageSpam), "messageSpam")
    # printPlotWithAverege(getAverege(messageHum), normilize(messageHum), "messageHum")

    saveToCsv(spamMap, "spam.csv")
    saveToCsv(humMap, "hum.csv")

def lab2Main():
    humCount = 0
    spamCount = 0
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in humreader:
            humCount=humCount+int(h[1])
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in spamreader:
            spamCount = spamCount + int(h[1])
    print(humCount)
    print(spamCount)
    print("Enter message")
    strn = str(input())
    print(strn)
    pat = re.compile(r'[^a-zA-Z ]+')
    strn = re.sub(pat, ' ', strn).lower()
    messageList=convertStringToListAndStem(strn)
    messageHumDict={}
    messageSpamDict = {}
    spam=0
    hum=0
    z=1;# коеф размытия

    humDictFromFile={}
    spamDictFromFile = {}
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for f in humreader:
            humDictFromFile[f[0]]=f[1]
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for f in spamreader:
            spamDictFromFile[f[0]]=f[1]

    for key in messageList:
        print(key)
        if key in humDictFromFile.keys():
            # messageHumDict.update({key: (int(humDictFromFile.get(key))+z) / (humCount+z*10)})
            messageHumDict.update({key: math.log((int(humDictFromFile.get(key))+z) / (humCount+z*10))})
        else:
            # messageHumDict.update({key: z/(humCount+z*10)})
            messageHumDict.update({key: math.log(z/(humCount+z*10)) })
    for key in messageList:
        print(key)
        if key in spamDictFromFile.keys():
            # messageSpamDict.update({key: (int(spamDictFromFile.get(key)) + z) / (spamCount+z*10)})
            messageSpamDict.update({key: math.log((int(spamDictFromFile.get(key)) + z) / (spamCount+z*10))})
        else:
            # messageSpamDict.update({key: z / (spamCount+z*10)})
            messageSpamDict.update({key:math.log(z / (spamCount+z*10))})
    for h in messageHumDict.values():
        hum=hum+h
    for h in messageSpamDict.values():
        spam=spam+h
    print("Hum:= " , hum)
    print("Spam=" , spam)
    print(hum/(hum+spam))
    if(hum/(hum+spam)<0.55):#от 0 до 0.55 скорее хам, от 0.55 до 1 спам
        print("It's hum, good")
    else:
        print("It's SPAM, NOOOOOO")




#lab1Main()
lab2Main()



