#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
from tqdm import tqdm

# 读取数据
with open('/content/output_256.pkl', 'rb') as f:
    data = pickle.load(f)

# 建立字典
result = {}
for max_value_theta_i, new_pixel_value, theta_new, x_value, y_value in data:
    index = (x_value, y_value)
    output = (new_pixel_value, theta_new)
    result[index] = output

# 加载.pkl文件
with open('/content/result_array.pkl', 'rb') as f:
    result_array = pickle.load(f)

# 建立数组
result_new = []

# 遍历数组并查询结果
with tqdm(total=len(result_array)) as pbar:
    for m, n in result_array:
        # 在字典result中查询结果
        if (m, n) in result:
            query_result = result[(m, n)]
        else:
            # 处理查询失败的情况
            query_result = result[(0, 0)]

        # 在这里可以对查询结果query_result进行操作
        # 例如，将其保存在新的数据包中
        # ...

        # 将查询结果保存在result_new数组中
        result_new.append(((m, n), query_result))
        pbar.update(1)  # 更新进度条

# 保存查询结果为数据包
with open('/content/query_results.pkl', 'wb') as f:
    pickle.dump(result_new, f)

print("保存成功！")

