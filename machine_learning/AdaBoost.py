from numpy import *
#对单树进行通过阀值预测进行分类
def StumpClassify(dataSet,dim ,theroldVal,flag):
    """
    :param dataSet: 单树的数据特征集合
    :param dim: 选取的数据中哪个特征位置
    :param theroldVal: 给定的一个分类的阀值
    :param flag:  预测为正确比较方法 2种：大于阀值的为正确的，小于等于阀值的为正确的。
    :return: 预测后的数据特征集合
    """
    m,n = shape(dataSet)
    #初始化预测结果的值都为正确的（1）
    classifyLabel = ones((m,1))
    if flag:
        classifyLabel[dataSet[:,dim] <= theroldVal] = -1
    else:
        classifyLabel[dataSet[:, dim] > theroldVal] = -1
    return classifyLabel

# 构建一个单树，标准是在给定权重的情况下，预测出来的误差率最小的那颗单树。
def buildStump(dataArr,classLabel,D):
    dataMat = mat(dataArr)
    labelMat = mat(classLabel).T
    m,n = shape(dataMat)
    minError = float(inf)
    bestStump ={}
    #初始化最佳分类
    bestClassify = mat(zeros((m,1)))
    for dim in range(n):
        minValue = dataMat[:,dim].min()
        maxValue = dataMat[:,dim].max()
        stepSize = (maxValue - minValue)/m
        # numSteps = 20
        # stepSize = (maxValue - minValue) / numSteps
        for j in range(-1 ,int(m) +1 ):
            theroldVal = minValue + stepSize*j
            for flag in [True,False]:
                predictClassifyLabel = StumpClassify(dataMat,dim,theroldVal,flag)
                errorArray = mat(ones((m,1)))
                errorArray[predictClassifyLabel == labelMat] = 0
                weightedError = D.T * errorArray
                if(weightedError < minError):
                    minError = weightedError
                    bestClassify =  predictClassifyLabel.copy()
                    bestStump['dim']= dim
                    bestStump['thresh'] = theroldVal
                    bestStump['flage'] = flag
    return minError,bestStump,bestClassify

# 算法的实现返回AdaBoos分类器
def AdaBoostTraining(dataSet,labelList,maxIter):
    classifyGroup = []
    dataMat = mat(dataSet)
    m,n = shape(dataMat)
    aggClass = mat(zeros((m, 1)))
    # 初始化样本的权重系数
    D = ones((m,1))/m
    for iter in range(maxIter):
        minError, bestStump, bestClassify = buildStump(dataSet,labelList,D)
        print('D:',D)
        alpha = float(0.5 * log((1.0 - minError)/max(minError,1e-16)))
        bestStump['alpha'] = alpha
        classifyGroup.append(bestStump)
        print('bestClassify',bestClassify)
        expon = multiply(-1 * alpha * mat(labelList).T,bestClassify)
        D = multiply(D ,exp(expon))
        D = D / sum(D)
        aggClass += alpha * bestClassify
        print('aggClass',aggClass)
        aggerror = multiply(sign(aggClass) != mat(labelList).T,ones((m,1)))
        print('aggerror',aggerror)
        errorRate = sum(aggerror) / m
        print('totalError',errorRate)
        if errorRate == 0.0 : break;
    return classifyGroup

def loadSimpData():
    dataMat=matrix([[1. ,2.1],
        [2. ,1.1],
        [1.3,1. ],
        [1. ,1. ],
        [2. ,1. ]])
    classLabels=[1.0,1.0,-1.0,-1.0,1.0]
    return dataMat,classLabels

if __name__ == '__main__':
    data, label = loadSimpData()
    classifierArr = AdaBoostTraining(data, label, 10)
    print(classifierArr)


























