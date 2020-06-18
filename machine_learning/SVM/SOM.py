from numpy import *

#启发式sMO算法的支持函数
#新建一个类的收据结构，保存当前重要的值
from SVM import selectAlpha


class optstruct:
    def __init__(self,dataMatIn,classLabels,C,toler, kTup):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.alphas=mat(zeros((self.m,1)))
        self.b=0
        self.Cache=mat(zeros((self.m,2)))

#格式化计算误差的函数，方便多次调用


def calcEk(os, k):
    '''计算预测误差'''
    fXk = float(multiply(os.alphas,os.labelMat).T*os.K[:,k] + os.b)
    Ek = fXk - float(os.labelMat[k])
    return Ek
#修改选择第二个变量alphaj的方法
def selectJ(i,os,Ei):
    maxK=-1;maxDeltaE= 0 ;Ej=0
    #将误差矩阵每一行第一列置1，以此确定出误差不为0
    #的样本
    os.Cache[i]=[1,Ei]
    #获取缓存中Ei不为0的样本对应的alpha列表
    validEcacheList=nonzero(os.Cache[:,0].A)[0]
    #在误差不为0的列表中找出使abs(Ei-Ej)最大的alphaj
    if(len(validEcacheList)>0):
        for k in validEcacheList:
            if k ==i:continue
            Ek=calcEk(os,k)
            deltaE=abs(Ei-Ek)
            if(deltaE>maxDeltaE):
                maxK=k;maxDeltaE=deltaE;Ej=Ek
        return maxK,Ej
    else:
    #否则，就从样本集中随机选取alphaj
        j=selectAlpha(i,os.m)
        Ej=calcEk(os,j)
    return j,Ej
#更新误差矩阵
def updateEk(os,k):
    Ek=calcEk(os,k)
    os.Cache[k]=[1,Ek]


def innerL(i,os):
    Eni = calcEk(os,i)
    if( (Eni*os.labelMat[i] < -os.tol and os.alpahs[i] <os.C ) or
            (Eni*os.labelMat[i] >  os.tol and os.alpahs[i] > 0 ) ):
       j,Enj =  selectJ(i, os, Eni)
       alphai_old = os.alpahs[i].copy()
       alphaj_old = os.alpahs[j].copy()
       if(os.labelMat[i]!=os.labelMat[j]):
           L = max(0, os.alphas[j] - os.alphas[i])
           H = min(os.C, os.C + os.alphas[j] - os.alphas[i])
       else:
           L = max(0, os.alphas[j] + os.alphas[i])
           H = min(os.C, os.alphas[j] + os.alphas[i] -os.C)
       if (L==H) : print('L equal H'); return 0
       eta = 2 * os.X[i].transposr()*os.X[j] - os.X[i].transposr()*os.X[i] -os.X[j].transposr()*os.X[j]
       if eta >= 0: print("eta>=0"); return 0
       os.alphas[j] -= os.labelMat[j] * (Eni - Enj) / eta
       from SVM import clipAlpha
       os.alphas[j] = clipAlpha(os.alphas[j], H, L)
       updateEk(os,j)
       if abs(alphaj_old - os.alpahs[j] <= 0.00001): return 0
       os.alpahs[i] += os.labelMat[i]*os.labelMat[j]*(alphaj_old - os.alpahs[j])
       updateEk(os,i)
       b1 = os.b - Eni - os.labelMat[i] * (os.alphas[i] - alphai_old) *os.X[i].transposr()*os.X[i] - os.labelMat[j] * (
                   os.alphas[j] - alphaj_old) * os.X[i].transposr()*os.X[j]
       b2 = os.b - Enj - os.labelMat[i] * (os.alphas[i] - alphai_old) * os.X[i].transposr()*os.X[j] - os.labelMat[j] * (
                   os.alphas[j] - alphaj_old) *os.X[j].transposr()*os.X[j]
       if (0 < os.alphas[i]) and (os.C > os.alphas[i]):
           os.b = b1
       elif (0 < os.alphas[j]) and (os.C > os.alphas[j]):
           os.b = b2
       else :
           os.b = (b2 +b1)/2
       return 1
    else : return  0

def smoP(dataSet,labelList,C,toler,maxIter):
    os = optstruct(dataSet,labelList,C,toler)
    iter = 0
    entireSet = True;
    alphaPairsChanged = 0
    while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet:  # go over all
            for i in range(os.m):
                alphaPairsChanged += innerL(i, os)
                print("fullSet, iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged))
            iter += 1
        else:  # go over non-bound (railed) alphas
            nonBoundIs = nonzero((os.alphas.A > 0) * (os.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i, os)
                print("non-bound, iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged))
            iter += 1
        if entireSet:
            entireSet = False  # toggle entire set loop
        elif (alphaPairsChanged == 0):
            entireSet = True
        print("iteration number: %d" % iter)




