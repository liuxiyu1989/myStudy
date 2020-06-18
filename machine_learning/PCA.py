from numpy import *


def loadDataSet(fileName, delim=' '):
    # fr = open(fileName)
    # stringArr = [line.strip().split(delim) for line in fr.readlines()]
    # datArr = [list(map(float,line)) for line in stringArr]
    # return mat(datArr)
    # 调用np的加载txt方法进行导入数据
    dataMate = loadtxt(fileName,dtype=float,delimiter=delim)
    return  mat(dataMate)

def replaceDataWithMean(fileName):
    dataMat = loadDataSet(fileName)
    numFeat = shape(dataMat)[1]
    for i in range(numFeat):
        meanVal = mean(dataMat[nonzero(isnan(dataMat[:,i])== False)[0],i])
        # print(meanVal)
        dataMat[nonzero(isnan(dataMat[:,i]))[0],i] = meanVal
    return  dataMat


def pca(dataMat,topFeat = 9999999):
    meanVal = mean(dataMat,axis=0)
    meanRemoved = dataMat - meanVal
    covVal = cov(meanRemoved)
    # print(covVal.shape)
    """
    特征向量：[λ1,0,0,0,0]
              [0,λ2,0,0,0]
              [0,0,λ3,0,0]
              [0,0,0,λ4,0] 
              [0,0,0,0,λ5] 
    """
    # 得到特征值数组和特征向量矩阵
    eigVals,eigMVects = linalg.eig(mat(covVal))
    sigIndex = argsort(eigVals)
    print(sigIndex.shape)
    sigIndex = sigIndex[:,-(topFeat+1):-1]
    eigMVectsTop = eigMVects[:sigIndex]

    # 得到另外转换后的空间
    transformSpace = meanRemoved * eigMVectsTop
    recData = transformSpace * eigMVectsTop.T +mean
    return  transformSpace,recData




if __name__ == '__main__':
    dataMat = replaceDataWithMean(r'D:\work\study\projectCode\untitled\examples\secom.data')
    pca(dataMat)








