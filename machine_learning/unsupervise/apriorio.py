from numpy import  *

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]


# 生成单个元素的数据项集
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    # py 3.0 map 是一个迭代器需要再次转化成list
    return list(map(frozenset, C1))

# 对所有的项集筛选出频繁项集
def scanD(D,CK,minsupport ):
    ssCnt = {}
    for S in D:
        for data in CK:
            if data.issubset(S):
                if not data in ssCnt.keys():
                    ssCnt[data] = 1
                else :ssCnt[data] += 1
    nums = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key] / nums
        if support >= minsupport:
            retList.insert(0,key)
            supportData[key] = support
    return retList , supportData

# 合并2个项集合生成含有K个单元素项集
def aprioriGen(LK,k):
    retList = []
    lenLK = len(LK)
    for i in range(lenLK):
        for j in range (i+1 ,lenLK):
            L1 = list(LK[i])[:k-2]
            L2 = list(LK[j])[:k-2]
            L1.sort()
            L2.sort()
            # 如果前k-2位相同合并
            if L1 == L2:
                retList.append(LK[i] | LK[j])
    return  retList

# 生成所有的满足频繁项集合
def apriori(dataSet,minSupport = 0.5):
    # 生成第一代项集（项集都是单个元素）
    C1 = createC1(dataSet)
    D = list(map(set ,dataSet ))
    k = 2
    L1, supportData = scanD(D,C1,minSupport)
    # print(L1)
    L = [L1]
    while len( L[k-2]) > 0:
        CK = aprioriGen(L[k-2],k)
        LK, nextData = scanD(D,CK,minSupport)
        # print(LK)
        #更新所有key对应的值
        supportData.update(nextData)
        L.append(LK)
        k+=1
    return L,supportData


# 生产关联规则
def generatorRules(L ,supportData,minConf = 0.7):
    return


# 计算可信度
def calConf(L,minConf=0.7):
    return




if __name__ == '__main__':
    dataSet = loadDataSet()
    assemble = createC1(dataSet)
    # for data in assemble:
    #     print(data,type(1))
    list,supportData = apriori(dataSet,0.7)
    # print(list)
    # print(supportData)
    for i in range(0, len(list)):
        for freqSet in list[i]:
            H1 = [frozenset([item]) for item in freqSet]
    print(len(H1[0]))
    print(H1)









