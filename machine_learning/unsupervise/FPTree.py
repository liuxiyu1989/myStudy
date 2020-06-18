class NodeTree:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.chirdren = {}

    def inc(self, numOccur):
        self.count += numOccur

     # 打印树的信息
    def disp(self, ind=1):
        print
        '  ' * ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind + 1)


# 创建树
def CreatePFTree(dataSet, minSup=1):
    # 初始化头指针表
    headerTable = {}
    # 对数据集中的每个元素进行统计次数
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    # 删掉小于最小支持度的数据集，成为频繁数据集项
    for k in headerTable:
        if headerTable[k] < minSup:
            del (headerTable[k])
    freqSet = set(headerTable.keys())
    # 如果没有满足最小支持度数据集项，则放回空的FP树和节点链接信息
    if len(freqSet) == 0: return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    # 初始化根树信息
    retTree = NodeTree("fir", 1, None)
    for trans, count in dataSet.items():
        localID = {}
        for k in trans:
            if k in freqSet:
                localID[k] = headerTable[k][0]
        if len(localID) > 0:
            # 一个数据项集（['r', 'z', 'h', 'j', 'p']）中的所有单元素计算出现的次数按照降序排序，存到字典里面
            # {r:2,z:1,h:1 ....}
            orderItems = [v[0] for v in sorted(localID.items(), key=lambda p: p[1], reverse=True)]
            # print(orderItems)
            # 更新树
            updateTree(retTree, orderItems, headerTable, count)
    return retTree, headerTable


# 更新树的节点对应的信息：父节点、子节点、以及每个项集中单元素出现次数和头部表等
def updateTree(tree, items, headerTable, count):
    """
    :param tree: FP树
    :param items: 已经对数据集单元素排过序的集合：（）
    :param headerTable:
    :param count:
    """
    if items[0] in tree.chirdren:
        tree.chirdren[items[0]].inc(count)
    else:
        tree.chirdren[items[0]] = NodeTree(items[0],headerTable[items[0]][0],tree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = tree.chirdren[items[0]]
        else:
            updateHeader(headerTable[items[0]][1],tree.chirdren[items[0]])
    if len(items) > 0:
        updateTree(items[1::],tree.chirdren[items[0]],headerTable,count)



# 更新头表单信息
def updateHeader(nodetoNest,targetNode):
    # 找到头表单信息最后一个指针指引的树节点地址
    while (nodetoNest.nodeLink != None):
        nodetoNest = nodetoNest.nodeLink
    # 再把刚刚加入进来相同的元素子节点信息链接到最后一个指针的后面。
    nodetoNest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

# 反向遍历所有的树中前向路径信息
def ascendTree(leafNode,prefixPath):
    if(leafNode.parent!= None):
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

# 得到对应这个树所有的前向路径（条件模式基）
def getPrefixPath(pabase,treeNode,):
    conpats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode,prefixPath)
        if len(prefixPath)>1 :
            conpats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return  conpats

# 找到对应这个树所有的频繁项集
def mineTree(inTree,headerTable,minsup,prefix,freqItemList):
    vlist = [ v[0] for v in sorted(headerTable.items(),key = lambda p :p[1])]
    for basePat1 in vlist:
        freqSet = prefix.copy()
        freqSet.add(basePat1)
        freqItemList.append(freqSet)
        # 得到下一次迭代的模式基
        basePatNext = getPrefixPath(basePat1,headerTable[basePat1][1])
        # 创建符合条件的频繁基项的PF树
        pfTree,header = CreatePFTree(basePatNext,minsup)
        if(header != None):
            mineTree(pfTree,header,minsup,freqSet,freqItemList)

def mineTweets(tweetArr, minSup=5):
    parsedList = []
    # for i in range(14):
    #     for j in range(100):
    #         parsedList.append(textParse(tweetArr[i][j].text))
    initSet = createInitSet(parsedList)
    myFPtree, myHeaderTab = CreatePFTree(initSet, minSup)
    myFreqList = []
    mineTree(myFPtree, myHeaderTab, minSup, set([]), myFreqList)
    return myFreqList




if __name__ == '__main__':
    data = loadSimpDat()
    dataSet = createInitSet(data)
    CreatePFTree(dataSet, 1)

