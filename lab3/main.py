# variables
import math
import random
from itertools import cycle

import numpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from scipy.spatial import distance

a=dict()
maxX=0
maxY=0

def getDistFromPointToPoint2(a1,a2):
    return distance.euclidean(a1, a2)

def getDistFromPointToPoint(a1,a2):
    return math.sqrt((a2[0]-a1[0])*(a2[0]-a1[0])+(a2[1]-a1[1])*(a2[1]-a1[1]))


def fromFileToNumList():
    global maxX, maxY
    f = open("s1.txt", "r")
    for x in f:
        if(maxX<int(x.split()[0])):
            maxX=int(x.split()[0])
        if(maxY<int(x.split()[1])):
            maxY=int(x.split()[1])
        a[int(x.split()[0])]=int(x.split()[1])

def drawGraf(centerAr_DictPoints):
    cycol = cycle('bgcmk')
    for centerPoint, points in centerAr_DictPoints.items():
        x = [*points.keys()]
        y =[*points.values()]
        plt.scatter(x,y,c=cycol.__next__(),s=2)
    for centerPoint, points in centerAr_DictPoints.items():
        plt.scatter([centerPoint[0]],[centerPoint[1]],c='r',s=20)
    plt.show()


def getNewCenter(points):
    summaX=0
    summaY =0
    for x,y in points.items():
        summaX=summaX+x
        summaY = summaY +y
    return (summaX / len(points),summaY/len(points))


def main():
    # centerPoints=dict()
    fromFileToNumList()
    print("Enter count of center")
    cenCount= int(input())
    centerAr_DictPoints=dict()
    counter=0
    for f in range(cenCount):
        centerAr_DictPoints[(random.randint(0,maxX),random.randint(0,maxY))]=dict()
    oldCenter_Points=dict()
    while(oldCenter_Points != centerAr_DictPoints):
        print("Main=",oldCenter_Points != centerAr_DictPoints)
        print("VAlues=",oldCenter_Points.values() != centerAr_DictPoints.values())
        oldCenter_Points = centerAr_DictPoints.copy()
        for x,y in a.items():
            minDist=1000000000000
            closerPoint=()
            for centerPoint,points in centerAr_DictPoints.items():
                nDist=getDistFromPointToPoint((x,y),centerPoint)
                if(nDist<minDist):
                    minDist=nDist
                    closerPoint=centerPoint
            centerAr_DictPoints[closerPoint][x]=y
        newCenterPoints=dict()
        for center,points in centerAr_DictPoints.items():
            newCentre=getNewCenter(points)
            newCenterPoints[newCentre]=points.copy()
        centerAr_DictPoints=newCenterPoints.copy()

    drawGraf(centerAr_DictPoints)


main()