#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import numpy as np

# 加载数据包
with open('/content/statistics_results.pkl', 'rb') as f:
    results = pickle.load(f)

# 初始化结果列表
processed_results = []

# 遍历每四个元组进行处理
for i in range(0, len(results), 4):
    # 取出第一个到第四个元组的m_mean和n_mean，并计算均值
    m_mean_values = [results[j][0][0] for j in range(i, i+4)]
    n_mean_values = [results[j][0][1] for j in range(i, i+4)]
    m_mean_new = np.mean(m_mean_values)
    n_mean_new = np.mean(n_mean_values)

    # 取出第一个到第四个元组的theta_new_variance，并找到最小值
    theta_new_variance_values = [results[j][1][1] for j in range(i, i+4)]
    theta_new_variance_update = np.min(theta_new_variance_values)
    # 取出最小值对应的theta_new_mean
    theta_new_mean_update = results[i + np.argmin(theta_new_variance_values)][1][0]

    # 取出第一个到第四个元组的new_pixel_value_variance，并找到最小值
    new_pixel_value_variance_values = [results[j][1][3] for j in range(i, i+4)]
    new_pixel_value_variance_update = np.min(new_pixel_value_variance_values)
    # 取出最小值对应的new_pixel_value_mean
    new_pixel_value_mean_update = results[i + np.argmin(new_pixel_value_variance_values)][1][2]

    # 将处理结果添加到结果列表中
    processed_results.append((m_mean_new, n_mean_new, theta_new_mean_update, theta_new_variance_update,
                              new_pixel_value_mean_update, new_pixel_value_variance_update))

# 保存结果为数据包
with open('/content/processed_results.pkl', 'wb') as f:
    pickle.dump(processed_results, f)

print("保存成功！")

