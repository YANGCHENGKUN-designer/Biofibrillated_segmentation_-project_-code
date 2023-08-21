#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# 加载数据包
with open('/content/processed_results.pkl', 'rb') as f:
    processed_results = pickle.load(f)

# 初始化坐标值和像素值列表
x_values = []
y_values = []
pixel_values = []

# 遍历每个处理结果
for result in processed_results:
    m_mean_new = int(result[0])
    n_mean_new = int(result[1])
    new_pixel_value_mean_update = result[4]

    # 转换坐标值
    x_values.append(m_mean_new)
    y_values.append(n_mean_new)  # 将Y坐标值取反，使左上角对应（0, 0）

    # 处理像素值
    if new_pixel_value_mean_update <= 25:
        pixel_values.append(0)
    else:
        pixel_values.append(new_pixel_value_mean_update)

# 将像素值转换为 NumPy 数组
pixel_values = np.array(pixel_values)

# 使用高斯滤波器进行处理
sigma = 0.5  # 高斯核的标准差
pixel_values_processed = gaussian_filter(pixel_values, sigma)

# 绘制图形
plt.scatter(x_values, y_values, c=pixel_values_processed, cmap='viridis')
plt.colorbar()
plt.gca().invert_yaxis()  # 反转Y轴，使左上角对应（0, 0）


# 保存图形为图片
plt.savefig('/content/plot.png')

# 显示图形
plt.show()

