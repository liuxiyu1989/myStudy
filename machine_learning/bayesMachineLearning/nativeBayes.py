import numpy as np
def createWordList(dataSet):
    wordList=set([])
    for words in dataSet:
        wordList = wordList| set(words)
    return  list(wordList)

def wordListToVector(wordList,inputWordList):
    vector = [0]*len(wordList)
    for word in inputWordList:
        if word in wordList:
            vector[wordList.index(word)]=1
    return vector


#对出现过的词不做统一的1处理，而是计算实际出现的次数
def bagOfWords2Vector(wordList,inputWordList):
    bagVector = [0] * len(wordList)
    for word in inputWordList:
        if word in wordList:
            bagVector[wordList.index(word)] += 1
    return bagVector

#判断一个文字集合中是否出现这个单词，转成向量级
def tansformToVector(data,classify):
    dims = data.shape
    transformData = np.zeros(dims)
    rows = dims[0]
    clos = dims[1]
    for i in range(rows):
        for j in range(clos):
            if data[i,j] == classify:
                transformData[i,j]=1
    return  transformData

# 计算一个给定的训练集的各个条件概率以及结果概率
def calculateBayesProb(trainDataSet,classifyRes):
    """
    :param trainDataSet: '训练集数据
    :param classifyRes: 训练集分类结果
    """
    number_words = len(trainDataSet[0])
    number_article = len(trainDataSet)
    #计算出结果集的概率 p(Y)
    prob_y=sum(classifyRes)/float(len(classifyRes))

    #计算出每个word在文档中出现的概率
    #初始化计算次数为1
    prob_number_xy_0= np.ones(number_words)
    prob_number_xy_1 = np.ones(number_words)
    #为防止没有出现概率为0的情况做一次平滑处理优化一下
    prob_sum_xy_0 = 2
    prob_sum_xy_1 = 2

    for i in range(number_article):
        #判断是哪一种分类计算这种结果下，单词出现的次数
        if classifyRes[i] ==1:
            prob_number_xy_1 = np.add(prob_number_xy_1, trainDataSet[i])
            prob_sum_xy_1 += sum(trainDataSet[i])
        else:
            prob_number_xy_0 =  np.add(prob_number_xy_0,trainDataSet[i])
            prob_sum_xy_0 += sum(trainDataSet[i])
    return np.log(prob_number_xy_0/prob_sum_xy_0),np.log(prob_number_xy_1/prob_sum_xy_1),prob_y


#对待测试的数据集进行预测，返回预测的分类结果
def predictBayes(testVector,p0,p1,prob_y):
    """
    :param testVector: 带预测的数据集转换后的向量
    :param p0: 预测结果为0的每个单词出现的概率
    :param p1: 预测结果为1的每个单词出现的概率
    :param prob_y: 预测结果为1的概率
    :return:
    """
   #贝叶斯公式取对数后的概率
    p_1 = sum (testVector*p1) + np.log(prob_y)
    p_0 =sum(testVector*p0) + np.log(1-prob_y)

    if p_1 >p_0 : return 1
    else : return  0



if __name__ == '__main__':
    data = np.loadtxt(r'D:\work\study\projectCode\untitled\examples\document.txt',dtype=str,delimiter=' ')
    # print(data)
    dataSet = np.ndarray.tolist(data)
    zeroVector = np.zeros(data.shape)
    wordList = createWordList(dataSet)
    # print(createWordList(dataSet))
    classVector = ['your','and','you','data'] # 表示这些单词带有激进的意思
    sampleRe = [0,1,0,0,0,1,1] # 表示样本最后评为是否是激进类型的文章
    # transformData = np.zeros(data.shape)
    # for vector in classVector:
    #     transformData += tansformToVector(data, vector)
    # print(transformData)
    dataMatrix=[]
    for words in dataSet:
        wordVector = wordListToVector(wordList, words)
        dataMatrix.append(wordVector)
    # print(dataMatrix)
    p0,p1,py = calculateBayesProb( np.array(dataMatrix),sampleRe)
    print(p0,p1,py)
    testWord=['your','you','and','yes','no','data']
    testWord1 = ['nobody', 'story', 'is', 'in', 'no', 'out']
    testVector  = wordListToVector(wordList,testWord)
    testVector1 = wordListToVector(wordList, testWord1)
    res = predictBayes(testVector,p0,p1,py)
    res1 = predictBayes(testVector1, p0, p1, py)
    print(res,res1)
    










