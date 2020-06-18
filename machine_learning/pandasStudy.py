
import pandas as pd

# 测试pandas的基本使用方法
def pandas_study ():
    print(series01.size)
if __name__ == '__main__':
   series01 = pd.Series({'苹果':0,'梨子':'1','香蕉':3})
   print(series01)
   series02 = pd.Series([1,0,1],index=['苹果','梨子','香蕉'])
   print(series02['苹果'])
   print("**************************")
   print(pd.isnull(series01))
   print(series01.reindex(['苹果','梨子','苹果']))
   print(series01.describe())
   print(series01.count())
   # series03 = series01.reindex(['苹果', '梨子', '苹果'])
   series01.describe().all



