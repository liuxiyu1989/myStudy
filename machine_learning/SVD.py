from numpy import  *
from  numpy import  linalg as la


"""
相似度计算方法：
1.求矩阵范数，加上类似平滑因子1
2.求2个向量的夹角，如果为90度则相关度为0，如为0相关度为1
3.求pearson 系数作为相关度（公式为 cov（A，B）/δA*δB）

"""
def ecludSim(inA,inB):
    return 1.0/(1.0+la.norm(inA-inB))

def cosSim(inA,inB):
    num = float(inA * inB)
    denom = la.norm(inA)*la.norm(inB)
    return 0.5 + 0,.5*num/denom

def peasronSim(inA,inB):
    if (len(inA)<3) :return 1.0
    pearsonCov = corrcoef(inA,inB,rowvar= False )[0][1]
    print(pearsonCov)
    return  0.5 +0.5*pearsonCov

# 标准相似度估计算法
def standEst(dataMat,user,simMeas,item):
    n = shape(dataMat)[1]
    simTotal = 0 ; simRateTotal = 0
    for i in range(n):
        # 获取不为0的评分数
        userRating = dataMat[user,i]
        # 减少循环次数，如果为0的话不需要参与下面的相似度计算了
        if userRating ==0: continue

        overlap = nonzero(logical_and(dataMat[:,item]>0,dataMat[:,i]>0))[0]
        if len(overlap)==0:
            simRate =0
        else :simRate = simMeas(dataMat[overlap,item],dataMat[overlap,i])
        simTotal += simRate
        simRateTotal += simRate*userRating
    if simTotal == 0: return  0
    else :return simRateTotal/simTotal


# 推荐算法
def recommend(dataMat,user,N=3,simMeas=cosSim,esMethod=standEst):
    """
    :param dataMat: 评分数据集
    :param user: 推荐的指定的用户
    :param N: 指定返回推荐的物品数量
    :param simMeas: 调用的相似度计算方法:
    :param esMethod: 调用推荐估算方法
    :return:用户推荐的物品以及估算评分数
    """
    n = shape(dataMat)[1]
    items = nonzero(dataMat[user,:]>0)[1]
    if len(items==0):return None
    itemScores = []
    for item in items:
        Essim = esMethod(dataMat,user,simMeas,item)
        itemScores.append((item,Essim))
    return sorted(itemScores,key=lambda d:d[1],reverse=False)[:N]


# 获取奇异特征值向量的个数
def getMainFeatrue(Sigma ,thereThold):
    SigmaSqr = Sigma ** 2
    total = sum(SigmaSqr)
    for i in range(len(Sigma)):
        if(sum(Sigma[:i]/total>thereThold)):return i


# 奇异特征矩阵变换后相似度算法
def SVDEst(dataMat,user,simMeas,item):
    n = shape(dataMat)[1]
    simTotal = 0; simRateTotal = 0
    U,Sigma,VT = la.svd(dataMat)
    # 求出主要特征值占比90%的总共的特征值
    N = getMainFeatrue(Sigma,0.9)
    diagSigma = eye(N)*Sigma[:N]
    # 算出降维后的数据矩阵
    dataItems = dataMat.T*U[:N]*diagSigma.I
    for i in range(n):
        # 获取不为0的评分数
        userRating = dataItems[user, i]
        # 减少循环次数，如果为0的话不需要参与下面的相似度计算了
        if userRating == 0: continue
        overlap = nonzero(logical_and(dataItems[:, item] > 0, dataItems[:, i] > 0))[0]
        if len(overlap) == 0:
            simRate = 0
        else:
            simRate = simMeas(dataItems[overlap, item], dataItems[overlap, i])
        simTotal += simRate
        simRateTotal += simRate * userRating
    if simTotal == 0:
        return 0
    else:
        return simRateTotal / simTotal



if __name__ == '__main__':
    inA = mat([1,2,4,5,6]).T
    inB = mat([3, 5, 8, 9, 8]).T
    peasronSim(inA,inB)


