import math
import operator
import pickle
import numpy as np
# 计算香农熵值
def calShannongEnt(dataSet):
    numEntries = len(dataSet) # 计算给定测试数据集合的大小
    labcounts ={ } # 初始化数据分类集合
    for featvec in  dataSet :
        currentLabel = featvec[-1] # 取数据集中的标签分类
        if currentLabel not in labcounts.keys():
           labcounts[currentLabel] = 0
           labcounts[currentLabel] += 1
        else:
            labcounts[currentLabel] += 1
    Ent =0.0 # 初始化熵的值为0
    for lab in labcounts :
        prob = float(labcounts[lab])/ numEntries  # numEntries 计算每一个分类的概率
        Ent -= prob * math.log(prob,2) # 香农熵值公式
    return  Ent

# 划分数据集的方法
def splitDateSet(dateSet,axis,featrueValue):
    retDateSet = [] # 初始化一个列表
    for featvec in dateSet :
        if featvec[axis] == featrueValue:
            newVec = featvec[:axis]
            newVec.extend(featvec[axis+1:])
            retDateSet.append(newVec)
    return retDateSet


# 选取最好的数据集划分方法
def choosebestSplitDataSet(dataSet):
    numFeatrues = len(dataSet[0]) - 1 # 获取特征值的数量
    baseEnt = calShannongEnt(dataSet) # 计算原始的数据集的信息熵
    gainEnt = 0.0 # 初始化新增信息熵值为0
    bestFeatrues = -1 # 初始化信息熵最好的特征初始位置为-1
    for i in range(numFeatrues):
        # featureValueList = [0,1]
        featureValueList = set([example[i] for example in dataSet])
        newEnv = 0.0
        # 计算划分后的信息熵值
        for featureValue in featureValueList :
            subDateSet = splitDateSet(dataSet,i,featureValue)
            prob = len(subDateSet)/float(len(dataSet))
            newEnv += prob * calShannongEnt(subDateSet)
        gain = baseEnt - newEnv  #初始的减去划分后的熵值
        if(gain > gainEnt):
           gainEnt =gain
           bestFeatrues = i
    return  bestFeatrues


# 选取特征相同数量最多的分类作为第k类决策树节点
# 使用多数表决法：若集合中属于第K类的节点最多，则此分支集合
# 划分为第K类
def chooseMaxVote(classList):
    classCount = { }
    for vote in classList:
        classCount[vote] = classCount.get(vote,0)+ 1
    sortClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse= True)
    return  sortClassCount[0][0] # 返回类别数量最多的类别名称


#创建决策树的方法
def Create_DTree(dataSet,labels):
    classList = [ example[-1] for example in dataSet ] # 提取数据集中的分类最终结果值
    if  classList.count(classList[0]) == len(classList): #如果分类结果只有一种|相同就返回
        return classList[0]
    if len(dataSet[0]) == 1:
        return chooseMaxVote(classList)
    bestFeatrue =  choosebestSplitDataSet(dataSet) # 选取最好的划分子集的特征
    bestLabelName = labels[bestFeatrue] #取的的标签名称
    tree ={ bestLabelName:{}}
    subLabels = labels[:]
    del [subLabels[bestFeatrue]]
    bestFeatrueList = [example[bestFeatrue] for example in dataSet ] #获取最好对应的标签分类的所有的特征值：
    unique_bestValue = set(bestFeatrueList) # 把重复的标签特征值去掉保留不同的分类特征值 比如标签为年龄，它的值有old，young，baby三种
    for featrueValue in unique_bestValue:
        tree[bestLabelName][featrueValue] = Create_DTree(splitDateSet(dataSet,bestFeatrue,featrueValue),subLabels)
    return tree


# 序列化和反序列化
def storeTree(inputTree,filename):
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)

def readTree(filename):
    fr = open(filename,'r')
    return  pickle.load(fr)



#用决策树进行判断和分类得出预测结果
def classifyDataSet(inputTree,labels,testData):
    firstFeatrue = inputTree.keys()[0]
    secondTree = inputTree[firstFeatrue]
    index = labels.index(firstFeatrue)
    for key in secondTree.keys():
        if testData[index] == key:
            if type(secondTree[key]).__name__ == 'dict':
                classLabel = classifyDataSet(secondTree[key],labels,testData)
            else:
                classLabel = secondTree[key]
    return classLabel


if __name__ == '__main__':
    dataSet1 = np.loadtxt(r'D:\work\study\projectCode\untitled\examples\lense.txt', dtype=str, delimiter='\t')
    dataSet2 = np.ndarray.tolist(dataSet1)
    print(dataSet2)
    print(dataSet1)
    # 这个是给定的特征标签
    labels = ['age','prescript','astigmatic','tearRate']
    print(labels)
    tree = Create_DTree(dataSet2,labels)
    print(tree)

