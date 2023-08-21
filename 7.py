#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import numpy as np

# 加载数据包
with open('/content/new_array.pkl', 'rb') as f:
    new_array = pickle.load(f)

# 初始化结果列表
results = []

# 遍历每一行
for row in new_array:
    # 提取每个元组的值
    theta_new_values = [item[1][0] for item in row]
    new_pixel_value_values = [item[1][1] for item in row]
    m_values = [item[0][0] for item in row]
    n_values = [item[0][1] for item in row]

    # 计算统计数据
    theta_new_mean = np.mean(theta_new_values)
    theta_new_variance = np.var(theta_new_values)
    new_pixel_value_mean = np.mean(new_pixel_value_values)
    new_pixel_value_variance = np.var(new_pixel_value_values)
    m_mean = np.mean(m_values)
    n_mean = np.mean(n_values)

    # 将结果添加到结果列表中
    results.append(((m_mean, n_mean), (theta_new_mean, theta_new_variance, new_pixel_value_mean, new_pixel_value_variance)))

# 保存结果为数据包
with open('/content/statistics_results.pkl', 'wb') as f:
    pickle.dump(results, f)

print("保存成功！")

