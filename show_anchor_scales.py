# -*- coding: utf-8 -*-
# @Time    : 20-2-13 下午5:03
# @Author  : wusaifei
# @FileName: Vision_data.py
# @Software: PyCharm

import pandas as pd
import seaborn as sns
import numpy as np
import json
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.family']='sans-serif'
plt.rcParams['figure.figsize'] = (10.0, 10.0)
import math

# 读取数据
ann_json = 'F:\\four_first\\train\\ship_train_1024.json'
with open(ann_json) as f:
    ann=json.load(f)

#################################################################################################
#创建类别标签字典
category_dic=dict([(i['id'],i['name']) for i in ann['categories']])
print(category_dic)
counts_label=dict([(i['name'],0) for i in ann['categories']])

for i in ann['annotations']:
    counts_label[category_dic[i['category_id']]]+=1 # "category_id": 5, i['category_id'] = 5 category_dic[5]='A220'
print(counts_label)

# 标注长宽高比例

box_area = []


for a in ann['annotations']:
    if a['category_id'] != 0:
        area = 10 * round(math.sqrt(a['area']) / 10, 0)
        box_area.append(area)

print(set(box_area))


# 所有标签的长宽高比例
box_area_unique = sorted(list(set(box_area)))
print(box_area_unique)
box_area_count=[box_area.count(i) for i in box_area_unique]

# 绘图
area_df = pd.DataFrame(box_area_count,index=box_area_unique,columns=['anchor_scales'])
area_df.plot(kind='bar',color="#55aacc")
plt.show()