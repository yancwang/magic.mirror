# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 11:39:43 2017

@author: yanc wang
@version: python2.7
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from six.moves import cPickle as pickle
from sklearn.cluster import KMeans

# import data
# read in csv file
filepath = 'C:/Users/yancw/Documents/Python Scripts/financedata/LC.csv';
lc = pd.read_csv(filepath);
print('Successful load data from LC.csv');
filepath = 'C:/Users/yancw/Documents/Python Scripts/financedata/LP.csv';
lp = pd.read_csv(filepath);
print('Successful load data from LP.csv');

# data preprocess
# checking missing values
lc.isnull().sum();
lp.isnull().sum();

# handling categorical data
# column 是否首标
# no: 0; yes: 1;
class_mapping = {'\xe5\x90\xa6': 0, '\xe6\x98\xaf': 1};
lc['是否首标'] = lc['是否首标'].map(class_mapping);
# column 性别
# female: 0; male: 1;
class_mapping = {'\xe5\xa5\xb3': 0, '\xe7\x94\xb7': 1};
lc['性别'] = lc['性别'].map(class_mapping);
# column 手机认证
# success: 0; unsuccess: 1;
class_mapping = {'\xe6\x88\x90\xe5\x8a\x9f\xe8\xae\xa4\xe8\xaf\x81': 0,
                 '\xe6\x9c\xaa\xe6\x88\x90\xe5\x8a\x9f\xe8\xae\xa4\xe8\xaf\x81': 1};
lc['手机认证'] = lc['手机认证'].map(class_mapping);
# column 户口认证
# success: 0; unsuccess: 1;
lc['户口认证'] = lc['户口认证'].map(class_mapping);
# column 视频认证
# success: 0; unsuccess: 1;
lc['视频认证'] = lc['视频认证'].map(class_mapping);
# column 学历认证
# success: 0; unsuccess: 1;
lc['学历认证'] = lc['学历认证'].map(class_mapping);
# column 征信认证
# success: 0; unsuccess: 1;
lc['征信认证'] = lc['征信认证'].map(class_mapping);
# column 淘宝认证
# success: 0; unsuccess: 1;
lc['淘宝认证'] = lc['淘宝认证'].map(class_mapping);
# column 借款类型
# 其他: 0; 普通: 1; 电商: 2; APP闪电: 3
class_mapping = {'\xe5\x85\xb6\xe4\xbb\x96': 0, '\xe6\x99\xae\xe9\x80\x9a': 1,
                '\xe7\x94\xb5\xe5\x95\x86': 2, 'APP\xe9\x97\xaa\xe7\x94\xb5': 3};
lc['借款类型'] = lc['借款类型'].map(class_mapping);
# characterize data
# column 借款类型
class_label = LabelEncoder();
temp = lc[['借款类型']].values;
temp[:, 0] = class_label.fit_transform(temp[:, 0]);
ohe = OneHotEncoder(categorical_features=[0]);
temp = ohe.fit_transform(temp).toarray();
temp = pd.DataFrame(temp);
# create one to n columns
lc['借款类型-其他'] = temp[0];
lc['借款类型-普通'] = temp[1];
lc['借款类型-电商'] = temp[2];
lc['借款类型-APP闪电'] = temp[3];
# column 初始评级
class_mapping =  {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5};
lc['初始评级'] = lc['初始评级'].map(class_mapping);
class_label = LabelEncoder();
temp = lc[['初始评级']].values;
temp[:, 0] = class_label.fit_transform(temp[:, 0]);
ohe = OneHotEncoder(categorical_features=[0]);
temp = ohe.fit_transform(temp).toarray();
temp = pd.DataFrame(temp);
# create one to n columns
lc['初始评级-A'] = temp[0];
lc['初始评级-B'] = temp[1];
lc['初始评级-C'] = temp[2];
lc['初始评级-D'] = temp[3];
lc['初始评级-E'] = temp[4];
lc['初始评级-F'] = temp[5];

# normalize data
# normalize function
def normalize_data(dataframe, column_name):
	column_max = max(dataframe[column_name]);
	dataframe[column_name] = dataframe[column_name] / column_max;
	pass
# normalize function
def normalize_age(dataframe, column_name):
	column_max = max(dataframe[column_name]);
	column_min = min(dataframe[column_name]);
	dataframe[column_name] = dataframe[column_name] / (column_max - column_min);
	pass
# column 借款金额
normalize_data(lc, '借款金额');
# column 借款期限
normalize_data(lc, '借款期限');
# column 借款利率
normalize_data(lc, '借款利率');
# column 年龄
normalize_age(lc, '年龄');
# column 历史成功借款次数
normalize_data(lc, '历史成功借款次数');
# column 历史成功借款金额
normalize_data(lc, '历史成功借款金额');
# column 总待还本金
normalize_data(lc, '总待还本金');

# create new column 还款率
lc['还款率'] = lc['历史正常还款期数'] / (lc['历史正常还款期数'] + lc['历史逾期还款期数']);
# drop null data
lc = lc.dropna()
# plot
plt.figure();
lc.plot.scatter(x = '还款率', y = '借款利率');

# clustering
# choose the best k
distortions = []
for i in range(1, 11):
	km = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=300, random_state=0);
	km.fit(lc[['还款率', '借款利率']]);
	distortions.append(km.inertia_);
plt.plot(range(1,11), distortions, marker='o');
plt.xlabel('Number of clusters');
plt.ylabel('Distortion');
plt.show();

# create clusters and plot
km = KMeans(n_clusters=6, init='k-means++', n_init=10, max_iter=300, tol=1e-04, random_state=0);
cluster = km.fit_predict(lc[['还款率', '借款利率']]);
print('Successful created clusters');
plt.figure();
color = ['lightgreen', 'red', 'lightblue', 'orange', 'yellow', 'black'];
for i in range(0, 6):
	plt.scatter(lc[cluster==i]['还款率'], lc[cluster==i]['借款利率'], s=5, c=color[i], marker='s', label='cluster'+ str(i));

# create processed dataframe
# delete unused columns
col = ['ListingId', '借款利率', '借款成功日期', '初始评级', '历史正常还款期数', '历史逾期还款期数', '还款率'];
for c in col: del lc[c];

# save data
filepath = os.path.join(os.getcwd(), 'data.pickle');
try:
	f = open(filepath, 'wb');
	save = {'data': lc.values, 'cluster': cluster};
	pickle.dump(save, f, pickle.HIGHEST_PROTOCOL);
	print('Successful save data to', filepath);
	del save  # hint to help gc free up memory
except Exception as e:
	print('Unable to save data to', filepath, ':', e);
