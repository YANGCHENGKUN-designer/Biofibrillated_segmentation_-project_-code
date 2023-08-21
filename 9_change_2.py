#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from PIL import Image
import pickle

# 加载数据包
with open('/content/processed_results.pkl', 'rb') as f:
    processed_results = pickle.load(f)

# 提取坐标和像素值
x_values = [int(result[0]) for result in processed_results]
y_values = [int(result[1]) for result in processed_results]
pixel_values = [result[4] if result[4] >= 20 else 0 for result in processed_results]


# 获取最大像素值和最小像素值
max_pixel_value = np.max(pixel_values)
min_pixel_value = np.min(pixel_values)

# 处理只有一个像素值的情况
if max_pixel_value == min_pixel_value:
    max_pixel_value += 1
    min_pixel_value -= 1

# 创建空白图像
image = Image.new("L", (256, 256))

# 根据坐标和像素值填充图像
for x, y, pixel_value in zip(x_values, y_values, pixel_values):
    # 将像素值映射到0-255的范围
    normalized_pixel_value = int((pixel_value - min_pixel_value) / (max_pixel_value - min_pixel_value) * 255)

    # 在图像上设置像素值
    image.putpixel((int(x), int(y)), normalized_pixel_value)


# 保存新的图片
image.save("/content/plot.png")

print("新的图片已保存为 plot.png。")



