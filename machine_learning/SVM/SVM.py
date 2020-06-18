from numpy import *
def selectAlpha(i,m):
    j=i
    while (i==j):
        j = int(random.uniform(0, m))
    return  j

def clipAlpha(aj,H,L):
    if aj > H : aj = H
    if aj < L : aj = L
    return aj


# 简化版的SOM算法
#1.简化了第一步计算出最坏的不满足条件的alpha作为第一个 2.简化了第二个alpha选取的步骤，选取标准应该是下降而不是随机挑
# 选其中任意一个作为第二个alpha参数
def simpleSOM(dataSet,labelList,tolerent,C,iterMax):
    """
    :param dataSet:
    :param labelList:
    :param tolerent:
    :param C:
    :param iterMax:
    :return:
    """
    dataMat = mat(dataSet)
    labeMat = mat(labelList)
    m,n = dataMat.shape
    #初始化系数
    alpha = zeros((m,1))
    b = 0
    iter = 0
    while(iter<iterMax):
        # 改变的alpha对数
        alphaPairsChanged = 0
        for i in range(m):
            #计算每个样本的误差值
            fxi = multiply(alpha,labeMat).T*dataMat.T*dataMat[i]+b
            eni = fxi -labeMat[i]
            #找出不符合KTT条件的需要优化的a系数进行优化
            if(eni*labeMat[i] < -tolerent and alpha[i] < C or  eni*labeMat[i] >tolerent and alpha[i] >0):
                j = selectAlpha(i,m)
                aj = alpha[j]
                ai = alpha[i]
                if(labelList[i] != labelList[j]):
                    L = max(0,aj-ai)
                    H = min(C,C+ai-aj)
                else:
                    L = max(0,ai+aj-C)
                    H =  min (C,ai+aj)
                if L==H:print('L==H') ; continue
                ai_old  = copy(ai)
                aj_old  = copy(aj)
                eta = 2 * dataMat[i]* dataMat[j].T - dataMat[i]*dataMat[i].T- \
                      dataMat[j]*dataMat[j].T
                fxj = multiply(alpha, labeMat).T * dataMat.T * dataMat[j] + b
                enj = fxj - labeMat[j]
                if eta >= 0 :print('eta is >= 0 the new alphaj is negative '); continue
                # 更新 alpha j 的值
                alpha[j] = labeMat[j]*(enj -eni)/eta
                alpha[j] = clipAlpha(alpha[j], H, L)
                if(abs(alpha[j] - aj_old) <= 0.00001 ):continue
                alpha[i] += labeMat[i]*labeMat[j](aj_old - alpha[j])
                # 再求b的值
                b1 = b - eni - labeMat[i] * (alpha[i] - ai_old) * dataMat[i] \
                     * dataMat[i].T - labeMat[j] * (alpha[j] - aj_old) * \
                     dataMat[i] * dataMat[j].T
                b2 = b - enj - labeMat[i] * (alpha[i] - ai_old) * \
                     dataMat[i] * dataMat[j].T - \
                     labeMat[j] * (alpha[j] - aj_old) * \
                     dataMat[j] * dataMat[j].T
                # 如果0<alphai<C,那么b=b1
                if (0 < alpha[i]) and (C > alpha[i]):
                    b = b1
                # 否则如果0<alphai<C,那么b=b1
                elif (0 < alpha[j]) and (C > alpha[j]):
                    b = b2
                # 否则，alphai，alphaj=0或C
                else:
                    b = (b1 + b2) / 2.0
                # 如果走到此步，表面改变了一对alpha值
                alphaPairsChanged += 1
                print("iters: %d i:%d,paird changed %d" % (iter, i, alphaPairsChanged))
                # 最后判断是否有改变的alpha对，没有就进行下一次迭代
                if (alphaPairsChanged == 0):
                    iter += 1
                # 否则，迭代次数置0，继续循环
                else:
                    iter = 0
                print("iteration number: %d" % iter)
                # 返回最后的b值和alpha向量
            return b, alpha





















