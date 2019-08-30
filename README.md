# python_data_cleaning
Summary of commonly used python data cleaning commands
# coding: utf-8

import pandas as pd 
import numpy as np

from scipy.interpolate import lagrange



#数据读取编码问题data= pd.read_csv(open(train_path,encoding='utf-8',errors='ignore'))



#自定义列向量插值函数
def ploy(s, n, k=6):
    if(s.shape[0] < 2*k + 1):
        print('不能用拉格朗日填充')
    elif(n-k < 0):
        y = s[list(range(0,n))+list(range(n + 1,2*k + 1))]
    elif(n + 1 + k > s.shape[0]):
        y = s[list(range(s.shape[0]- 1 - 2*k, n))+list(range(n + 1,s.shape[0]))]
    else:
        y = s[list(range(n - k, n))+list(range(n + 1, n + 1 + k))]
    y = y[y.notnull()]
    return lagrange(y.index, list(y))(n)



def fill_lagrange(col, k=5):
    #col = s.copy()
    for i in range(0, col.shape[0]):
        if(col.isnull()[i]):
            col[i] = ploy(col, i, k)
    print('the dataframe null_value filled by lagrange of '+str(k)+' step size')
            


def data_predeal(data):
    print('数据大小(行数，列数): ', data.shape,'\n')
    print('缺失值情况：')
    s = [[i,data[i].isnull().sum()] for i in list(data) if data[i].isnull().sum()!=0]
    print(s, '\n')
    print('数据基本描述:', '\n', data.describe())


def box_outlier(data,col_name):
    Q1 = np.percentile(data[col_name][-data[col_name].isnull()], 25)
    # 3rd quartile (75%)
    Q3 = np.percentile(data[col_name][-data[col_name].isnull()], 75)
    # Interquartile range (IQR)
    IQR = Q3 - Q1
    # outlier step
    outlier_step = 1.5 * IQR
    # Determine a list of indices of outliers for feature col
    outlier_list_col = (data[col_name] < Q1 - outlier_step) | (data[col_name] > Q3 + outlier_step )
    s = np.where(outlier_list_col == 1)[0].tolist()
    count=outlier_list_col.sum()
    return count, s



# 箱线图确定各列是否存在异常值，数目，及对应索引
def box_outlier_ps(data, col_list):
    a=[]
    b=[]
    for i in col_list:
        count, s = box_outlier(data, i)
        a.append([i,count])
        b.append(s)
    print(a)
    return a,b
