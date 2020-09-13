import csv
import math
import re

from nltk import PorterStemmer
from nltk.corpus import stopwords

porter = PorterStemmer()


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


def deleteSpecialSymbolsFromString(string):
    string = re.sub('[^a-zA-Z \n]', ' ', string)
    return convertStringToListAndStem(string)


def lab2Main():
    humCount = 0
    spamCount = 0
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in humreader:
            humCount = humCount + int(h[1])
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in spamreader:
            spamCount = spamCount + int(h[1])
    messageHumDict = {}
    messageSpamDict = {}
    spam = 0
    hum = 0
    z = 1;  # коеф размытия

    humDictFromFile = {}
    spamDictFromFile = {}
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for f in humreader:
            humDictFromFile[f[0]] = f[1]
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for f in spamreader:
            spamDictFromFile[f[0]] = f[1]
    while (True):
        print("Enter message")
        strn = str(input())
        messageList = deleteSpecialSymbolsFromString(strn)
        for key in messageList:
            if key in humDictFromFile.keys():
                # messageHumDict.update({key: (int(humDictFromFile.get(key))+z) / (humCount+z*10)})
                messageHumDict.update({key: math.log((int(humDictFromFile.get(key)) + z) / (humCount + z * 10))})
            else:
                # messageHumDict.update({key: z/(humCount+z*10)})
                messageHumDict.update({key: math.log(z / (humCount + z * 10))})
        for key in messageList:
            if key in spamDictFromFile.keys():
                # messageSpamDict.update({key: (int(spamDictFromFile.get(key)) + z) / (spamCount+z*10)})
                messageSpamDict.update({key: math.log((int(spamDictFromFile.get(key)) + z) / (spamCount + z * 10))})
            else:
                # messageSpamDict.update({key: z / (spamCount+z*10)})
                messageSpamDict.update({key: math.log(z / (spamCount + z * 10))})
        for h in messageHumDict.values():
            hum = hum + h
        for h in messageSpamDict.values():
            spam = spam + h
        # print("Hum:= ", hum)
        # print("Spam=", spam)
        # print(hum / (hum + spam))
        if (hum / (hum + spam) < 0.50):  # от 0 до 0.55 скорее хам, от 0.55 до 1 спам
            print("It's hum, good")
        else:
            print("It's SPAM, NOOOOOO")


lab2Main()
