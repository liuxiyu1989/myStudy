
from  numpy import *
# 找零钱问题
def countWays(dataset,pennysize,pennySum):
    """
    :param dataset: 零钱的种类
    :param pennysize: 找的零钱最大种数量
    :param pennySum:  找零钱的总量
    :return: 有多少种方法符合找总共为pennySize的零钱数额方法。

    """
    if (pennysize==0 or len(dataset)==0 or pennySum<0): return 0
    dp = zeros((pennysize,pennySum+1),dtype=int)
    # 初始化转态方程值
    dp[:,0] = 1
    for i in range(int(pennySum/dataset[0])):
        dp[0,i*dataset[0]] = 1
    # print(dp)
    for i in range(pennysize):
        for j in range(pennySum+1):
            if (j>=dataset[i]): dp[i,j] = dp[i-1,j] + dp[i,j -dataset[i]]
            else: dp[i,j] = dp[i-1,j]
    # print(dp)
    return dp[pennysize-1,pennySum]

# 01背包问题
def bag_dp(p,w,n,storage):
   v =  [[0 for i in range( storage+ 1)] for i in range(n + 1)]
   for i in range(1,n+1):
       for j in range(1,storage+1):
           if w[i-1] > j:
             v[i][j] = v[i-1][j]
           else:
             tmp1 =  v[i-1][j-w[i-1]] + p[i-1]
             tmp2 =  v[i-1][j]
             v[i][j] = max(tmp1,tmp2)

   return v


# 优化背包空间只存储最优的转态结果，把二维变为一维
def bagOpt(p,w,n,storage):
    v = [0 for i in range(storage+1)]
    for i in range(1, n + 1):
        for j in range(1, storage + 1):
            if(w[i-1] < j):
                v[j] = max( v[j-w[i-1]] + p[i-1] ,v[j]  )
    return v




if __name__ == '__main__':
    dataset = [1,2,4]
    # print(countWays(dataset,3,2))
    p = [1,3,10,20]
    w = [2,4,6,8]
    n = 4
    storage = 10
    # print(bag_dp(p, w, n, storage))
    print(bagOpt(p,w,n,storage))


