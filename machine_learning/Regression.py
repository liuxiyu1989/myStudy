from numpy import *


#标准线性回归预测算法
def StandReg(dataSet,labeList):
    xMat = mat(dataSet)
    yMat = mat(labeList).T
    xTxMat = xMat.T * xMat
    # 取行列式不为0才能可逆
    if linalg.det(xTxMat) == 0:
        print( '矩阵不可逆，不能够转换' )
        return
    ws = xTxMat.I * (xMat.T * yMat)
    return ws

#局部加权线性回归预测算法，对平均方差进行改善，是误差更小。
def WieghtReg(dataSet, labeList):
    xMat = mat(dataSet)
    yMat = mat(labeList).T





