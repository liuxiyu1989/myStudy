from nativeBayes import *
import  random
import re

def textPharse(String):
    wordsList = re.split(r'\W*',String)
    return [ word.lower() for  word in wordsList if len(word)>2]

def trainMail():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        wordList = textPharse(open(r'D:\work\study\projectCode\untitled\examples\spam\%d.txt'% i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textPharse(open(r'D:\work\study\projectCode\untitled\examples\ham\%d.txt' % i).read())
        docList.append(wordList)
        classList.append(0)
        fullText.extend(wordList)
    wordsList =createWordList(docList)

    #随机抽取40个为训练样本
    trainSet = list(range(50))
    testSet = []
    for i in range(10):
        randindex = int(random.uniform(0,len(trainSet)))
        testSet.append(trainSet[randindex])
        del(trainSet[randindex])
    trainMat = []
    trainClass= []
    for index in trainSet:
        trainMat.append(wordListToVector(wordsList,docList[index]))
        trainClass.append(classList[index])
    p0,p1,py = calculateBayesProb(trainMat,trainClass)

    errorCount = 0
    for index in testSet:
        wordVector = wordListToVector(wordsList,docList[index])
        if predictBayes(wordVector,p0,p1,py) != classList[index]:
            errorCount +=1

    print('误差为：',float(errorCount)/len(trainSet))
if __name__ == '__main__':
    trainMail()






