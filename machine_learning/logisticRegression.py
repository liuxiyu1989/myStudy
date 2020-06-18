import numpy as np
import matplotlib.pyplot as plt
# sigma函数
def sigmo(x):
    return  1.0 /(1+ np.exp(-x))

def loadData(fileName):
    dataSet = [];labeList = []
    fr = open(fileName)
    for readLine in fr.readlines():
        line = readLine.strip().split()
        # 数据类型为float，统一数字类型，方便后面的计算
        dataSet.append([1.0,float(line[0]),float(line[1])])
        labeList.append(line[-1])
    return dataSet,labeList


# 梯度上升算法
def grandDescent(dataSet,classLables):
    dataMat = np.mat(dataSet)
    m,n =dataMat.shape
    labelMat =  np.mat(classLables,dtype=np.float).transpose()
    weight = np.ones((n,1))
    alpha = 0.001
    maxCount = 500
    for k in range(maxCount):
       z = np.dot(dataSet,weight)
       # 求出每一个样本的误差
       error = labelMat - sigmo(z)
       # dataMat.transpose()* error 求出每一个特征系数,也就是求出梯度下降最快的特征方向（θ1，θ2，θ3，θ4）
       # 装置的目的就是求对应的特征系数
       weight =weight +alpha * dataMat.transpose()* error
    return  weight

# 随机梯度算法 减少计算量的优化版本,但是迭代的数量限于样本的数量，如果样本的数量过小导致没有收敛结束了
def randomGrandDescent(dataSet,classLables):
    dataMat = np.mat(dataSet)
    m, n = dataMat.shape
    labelMat = np.mat(classLables, dtype=np.float)
    weights = np.ones((n, 1))
    alpha = 0.01
    for i in  range(m):
        z = dataMat[i] * weights
        error = labelMat[(0,i)] -sigmo(np.sum(z))
        # 针对一个样本的值进行更新权重值
        weights = weights + alpha * error*dataMat[i].transpose()
    return  weights


# 随机梯度算法改进型 优化步长，增加衰减因子
def randomGrandDescent1(dataSet,classLables,maxCount):
    dataMat = np.mat(dataSet)
    m, n = dataMat.shape
    labelMat = np.mat(classLables, dtype=np.float)
    weights = np.ones((n, 1))
    for i in range(maxCount):
        for j in range(m):
            alpha = 4/(1+i+j)+0.01
            z = dataMat[j] * weights
            error = labelMat[(0, j)] - sigmo(np.sum(z))
            # 针对一个样本的值进行更新权重值
            weights = weights + alpha * error * dataMat[j].transpose()
    return weights


# 用图形化界面展示分界线
def plotBestFit(data, labelMat, weights):
    dataArr = np.array(data)
    n = np.shape(dataArr)[0]
    x_cord1 = [];
    y_cord1 = []
    x_cord2 = [];
    y_cord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            x_cord1.append(dataArr[i, 1]);
            y_cord1.append(dataArr[i, 2])
        else:
            x_cord2.append(dataArr[i, 1]); y_cord2.append(dataArr[i, 2])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_cord1, y_cord1, s=30, c='red', marker='s')
    ax.scatter(x_cord2, y_cord2, s=30, c='green')
    # 画出边界线的公式 θ1*x1+θ2*x2+θ3*x3 =0  其中x2 =x x3 =y x1=1(数据第一个特征本来就恒等于1)
    x = np.arange(-3.0, 3.0, 0.1)
    y = ((-weights[0] - weights[1] * x) / weights[2]).transpose()
    ax.plot(x, y)
    plt.xlabel('X1');
    plt.ylabel('X2');
    plt.show()





if __name__ == '__main__':
    fileName = r'D:\work\study\projectCode\untitled\examples\logisticTest.txt'
    dataSet,labeList =  loadData(fileName)
    # weights = grandDescent(dataSet, labeList)
    # print(weights)
    # weights = randomGrandDescent(dataSet,labeList)
    # print(weights)
    weights = randomGrandDescent1(dataSet,labeList,150)
    print(weights)
    plotBestFit(dataSet,labeList,weights)







