from numpy import  *
import matplotlib.pyplot as plt
# 注意为什么取最后一列解释：
# 这个计算预测成最后分来结果值的平均值，
# 前提是最后一列存的是数据集最后分类的结果值，
# 其他的列为每个特征值
def regMeanErr( dataSet ):
    return  mean(dataSet[:,-1])

def regErr(dataSet):
    return  var(dataSet[:,-1]) * shape(dataSet)[0]


# 按照某个特征值划分特征数据集合
def binSplitDataSet(dataSet ,feature , feaValue ):
    mat0 = dataSet [ nonzero( dataSet[:,feature] > feaValue )[0],:]
    mat1 = dataSet[nonzero(dataSet[:, feature] <= feaValue)[0], :]
    return  mat0,mat1


# 常规的递归创建回归树
def creatTree(dataSet,leafTtpe = regMeanErr ,errType = regErr,ops = (1,4)):
    bestFeatIndex,bestFeatValue = chooseBestSplit(dataSet,leafTtpe,errType,ops)
    if bestFeatIndex == None : return bestFeatValue
    resTree = { }
    resTree['spInd'] = bestFeatIndex
    resTree['spVal'] = bestFeatValue
    mat0 ,mat1 = binSplitDataSet(dataSet,bestFeatIndex,bestFeatValue)
    resTree['left'] = creatTree(mat0 , leafTtpe ,errType ,ops)
    resTree['right']  = creatTree(mat1 , leafTtpe ,errType ,ops)
    return  resTree


def chooseBestSplit ( dataSet , leafType = regMeanErr ,errType = regErr ,ops = (1,4) ):
    """

    :param dataSet: 数据集合
    :param leafType: 计算平均值
    :param errType: 选取计算误差的类型（标准方差作为类型）
    :param ops: 选取最好的子数分割的截止条件（平均方差）
    :return: 返回回归树（以字典的形式存放）
    """
    tolS = ops[0]
    tolN = ops[1]
    bestErr = inf;bestFeatValue = 0;bestFeatIndex = 0;
    if len(set(dataSet[:, -1].T.tolist()[0])) == 1 :
        return None,leafType(dataSet)
    m,n = shape (dataSet)
    S = errType(dataSet)
    bestS = inf ; bestIndex = 0 ; bestValue = 0
    # 开始进行选取最好的分割的特征值
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex].T.tolist()[0]):
           mat0, mat1 = binSplitDataSet(dataSet,featIndex,splitVal)
           if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
           err = errType(mat0) + errType(mat1)
           if(err<bestErr):
               bestErr = err
               bestFeatValue = splitVal
               bestIndex = featIndex
    if (S - bestErr) < tolS:
        return None,leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestFeatValue)
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
        return None,leafType(dataSet)
    return bestIndex,bestFeatValue


# 判断数据集是否为树，以类型为字段作为依据（有点不准，应该还要包括含有自己规定固定的key才行 ）
def isTree(tree):
    has = False
    if isinstance(tree,dict):
        # if( 'right'in tree.keys() and 'left' in tree.keys() ):
            has =True
    return has

# 获得叶子点的划分的阀值
def getMean( tree ):
    if isTree(tree['right']): tree['right'] = getMean( tree['right'] )
    if isTree(tree['left']): tree['left'] = getMean( tree['left'] )
    return (tree['right'] + tree['left']) /2.0

# 剪枝
def prune(tree,testData):
    if (shape(testData)[0] == 0):return getMean(tree)
    if(isTree(tree['right']) or isTree(tree['left'])):
        lData,rData = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if (isTree( tree['left'])): tree['left'] = prune(tree['left'],lData)
    if (isTree(tree['right'])):  tree['right'] = prune(tree['right'] ,rData )
    if( not isTree(tree['left']) and   not isTree(tree['right']) ):
        lData, rData = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        # 计算分割后没有合并的误差
        errorNoMerger = sum(power((lData[:,-1] - tree['left']),2)) + \
        sum(power((rData[:, -1] - tree['right']), 2))
        # 计算合并后的误差
        meanValue = getMean(tree)
        errorMerger = sum(power(testData[:,-1] - meanValue,2))
        if errorMerger < errorNoMerger:
            print('merging')
            return meanValue
        else : return tree
    else:return  tree

# 模型树剪枝
def modelPrune(tree,testData):
    m ,n = shape(testData)
    if (shape(testData)[0] == 0):return getMean(tree)
    if(isTree(tree['right']) or isTree(tree['left'])):
        lData,rData = binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if (isTree( tree['left'])): tree['left'] = modelPrune(tree['left'],lData)
    if (isTree(tree['right'])):  tree['right'] = modelPrune(tree['right'] ,rData )
    if( not isTree(tree['left']) and   not isTree(tree['right']) ):
        lData, rData = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        lXMat = mat(ones(shape(lData)))
        lXMat[:,1:n] = lData[:,0:n-1]
        # lYMat = mat (ones([shape(lData)[0],1]))
        rXMat = mat(ones(shape(rData)))
        rXMat[:, 1:n] = rData[:, 0: n - 1]
        # rYMat = mat(ones([shape(rData)[0], 1]))
        # 计算分割后没有合并的误差
        errorNoMerger = sum(power((lData[:,-1] - lXMat * tree['left']),2)) + \
        sum(power((rData[:, -1] - rXMat * tree['right']), 2))
        # 计算合并后的误差
        Ws = leafModel(testData)
        XMat = mat(ones([m,n]))
        XMat [:,1:n] = testData[:,0:n-1]
        errorMerger = sum(power(testData[:,-1] -  XMat * Ws ,2))
        if errorMerger < errorNoMerger:
            print('merging')
            return Ws
        else : return tree
    else:return  tree

def regModelErr(dataSet):
    W, X, Y = lineRegression(dataSet)
    return sum(power(  Y - X*W ,2 ))

def leafModel(dataSet):
    W, X, Y = lineRegression(dataSet)
    return  W

def lineRegression(dataSet):
      m,n = shape(dataSet)
      X =  mat(ones( [m,n] ))
      Y =  mat(ones( [m ,1]))
      X[:,1:n] = dataSet[:,0:n-1]
      Y = dataSet[:,-1]
      tx = X.T * X
      if linalg.det(tx) == 0.0:
          raise NameError( "矩阵为奇异矩阵，不可逆，增大ops的第二个参数即树叶子数据集")
      W = tx.I * X.T * Y
      return W,X,Y


def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        # map all elements to float()
        fltLine = list(map(float,curLine))
        dataMat.append(fltLine)
    return dataMat



if __name__ == '__main__':
    # dataSet = eye(4)
    # mat0 , mat1 = binSplitDataSet(dataSet , 2 , 0.2)
    # print(mat0,mat1,shape(mat1)[0])
    # data = loadDataSet(r'examples/resTree/ex0.txt')
    # dataSet = mat(data)
    # dataSet = array(data)
    # print(dataSet)
    # resTree =  creatTree(dataSet)
    # print(resTree)
    data = loadDataSet(r'examples/resTree/ex2.txt')
    dataSet = mat(data)
    dataArray = array((data))
    # regModelErr(dataSet)
    #
    # print(regModelErr(dataSet))

    # resTree = creatTree(dataSet,leafTtpe= leafModel , errType =regModelErr,ops=(1,10))
    # print(resTree)
    # data1 = loadDataSet(r'examples/resTree/ex2test.txt')
    # testDataSet = mat(data1)
    # prunedtree =  modelPrune(resTree,testDataSet)
    # print(prunedtree)

    plt.scatter(dataArray[:, 0], dataArray[:, 1])
    plt.show()



