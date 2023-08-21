#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import matplotlib.pyplot as plt
import numpy as np

# 加载数据包
with open('/content/processed_results.pkl', 'rb') as f:
    processed_results = pickle.load(f)

# 提取坐标和像素值
x_values = [int(result[0]) for result in processed_results]
y_values = [int(result[1]) for result in processed_results]
pixel_values = [result[4] if result[4] >= 20 else 0 for result in processed_results]

# 确定图像大小
width = max(x_values) + 1
height = max(y_values) + 1

# 创建空白图像
image = np.zeros((height, width))

# 将像素值填充到图像中的对应位置
for x, y, pixel in zip(x_values, y_values, pixel_values):
    image[y, x] = pixel

# 绘制图像
plt.imshow(image, cmap='viridis')
plt.axis('off')  # 隐藏坐标轴和刻度

# 保存图像为图片
plt.savefig('/content/plot.png', bbox_inches='tight', pad_inches=0)


