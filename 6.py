#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle

# 加载数据包
with open('/content/query_results.pkl', 'rb') as f:
    query_results = pickle.load(f)

# 统计元组的数量
count = 0
for item in query_results:
    if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], tuple) and isinstance(item[1], tuple):
        count += 1

print("元组的数量:", count)



import pickle
import numpy as np

# 加载数据包
with open('/content/query_results.pkl', 'rb') as f:
    query_results = pickle.load(f)

# 计算P和L
total_elements = len(query_results)
L = 5
P = total_elements // L

# 创建新数组
new_array = np.empty((P, L), dtype=object)

# 将元组放入新数组
index = 0
for item in query_results:
    if index >= P * L:
        break
    new_array[index // L, index % L] = item
    index += 1

# 打印新数组
for row in new_array:
    print(row)

# 保存新数组为数据包
with open('/content/new_array.pkl', 'wb') as f:
    pickle.dump(new_array, f)

print("保存成功！")

