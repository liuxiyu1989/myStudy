from numpy import  *
import matplotlib.pyplot as plt

# 计算点与点之间的距离
def oulaDistance(va,vb):
    return  sqrt(sum(power(va-vb,2)))

# 选取质心
def randCent(dataSet,k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range ( n ):
        dmin = min(dataSet[:,j ])
        drange = float ( max(dataSet[:,j]) - dmin )
        centroids[:,j] = dmin + drange * random.rand(k,1)
    return centroids

# 加载数据
def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        # map all elements to float()
        fltLine = list(map(float,curLine))
        dataMat.append(fltLine)
    return dataMat

# 基础Kmeas算法
def kMean( dataSet,k,distMeas = oulaDistance , createCent = randCent ):
    """

    :param dataSet: 数据集
    :param k: 选取质心个数
    :param distMeas: 计算点的距离方法
    :param createCent: 选取质心方法
    :return:
    """
    m,n = shape(dataSet)

    # 记录分类后的数据离质心最近的质心的位置以及离最近质心的距离
    clusterpos = mat(zeros(( m ,2)) )

    # 循环标志
    clusterChanged = True

    # 随机创建质心集合 k为自己指定的数量，此为初始质心信息。
    cents = randCent(dataSet , k)
    while clusterChanged:
        # 外循环目的记录所有数据集合离本次最近的质心存在clusterChanged
        # 如果分类的数据还有变动，更新一次质心信息，其取值方法：取离对应最近质心的所有数据集合中的特征向量各个平均值
        for i in range(m):
            # 初始化最小距离和离数据最近质心的位置
            disMin = inf  ; centindex = -1
            for j in range(k):
                dis =  distMeas(cents[j ,:] ,dataSet[ i ,: ])
                if dis < disMin:
                    disMin = dis
                    centindex = j
            if clusterpos[i,0] == centindex : clusterChanged =False
            clusterpos[i,:] = centindex ,disMin ** 2
        # 更新质心信息以及位置信息
        for centIndex in range(k):
            cluster = dataSet[nonzero( clusterpos[:,0] == centIndex )[0]]
            # axis =0  压缩行 对每列特征值进行平均
            cents[centIndex,:] = mean(cluster,axis= 0)
    # 没有更新退出得出最合适的质心和信息
    return cents,clusterpos

# dichotomy 二分法Kmeans
def diKmeans(dataSet, k,distMeas = oulaDistance):
    m,n = shape(dataSet)
    # 计算作为一个类簇的质心
    cents =  mean(dataSet,axis = 0)
    cents0 = mean(dataSet, axis=0).tolist()[0]
    centsList = [cents0]
    # 记录分类后的数据离质心最近的质心的位置以及离最近质心的距离
    clusterpos = mat(zeros((m, 2)))
    # 计算初始没有分的信息
    for j in range (m):
        clusterpos[j,1] = distMeas(dataSet[j,:],cents)
    # 只要指定分类数量没有超过k，就需要进行二分法，选取二分子类最好的添加到质心中去
    while len(centsList) < k:
        # 对每次分类后的进行二分
        for i in range(len(centsList)):
            # 初始化误差
            disMin = inf ; bestsplitIndex = -1
            centsplt, clusterplitpos = kMean(dataSet,2,distMeas = oulaDistance)
            # 计算选取已分的误差总和
            splitdis = sum(clusterplitpos[:,1])
            # 计算选取没有分的误差总和
            nosplitdis = sum(clusterpos(nonzero(clusterpos[:, 0] != i))[1])
            print("splitdis, and nosplitdis: ",)
            if (splitdis + splitdis) < disMin:
                bestsplitIndex = i
                disMin = splitdis + splitdis
                bestCents = centsplt
                bestclusterpos  =clusterplitpos.copy()
        # 对选最好的进行更新信息
        # 把第二个分好的类更新成最后一个质心位置
        bestclusterpos[nonzero(bestclusterpos[:,1] == 1)[0],0] = len(list)
        # 把第二个分好的类第一个变成分割最好的质心位置
        bestclusterpos[nonzero(bestclusterpos[:, 1] == 0)[0],0] = bestsplitIndex

        # 更新质心信息
        centsList[bestsplitIndex] = bestCents[1:]
        centsList.append(bestCents[0:].tolist()[0])

        # 更新质心位置信息
        clusterpos[nonzero(clusterpos[:0] == bestsplitIndex)[0],:] = bestclusterpos
    return mat(centsList),clusterpos


if __name__ == '__main__':
    data = loadDataSet( r'D:\work\study\projectCode\untitled\examples\Kmeans\testSet.txt')
    dataSet = mat(data)
    cents, clusterpos = kMean(dataSet,4)
    print(cents,clusterpos)
    dataArray = array((data))
    # plt.scatter(dataArray[:, 0], dataArray[:, 1])
    # plt.show()




































