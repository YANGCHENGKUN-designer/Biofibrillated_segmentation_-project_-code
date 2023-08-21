#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from PIL import Image
import pickle

# 加载数据包
with open('/content/processed_results.pkl', 'rb') as f:
    processed_results = pickle.load(f)

# 定义像素值处理函数
def process_pixel_value(value):
    if value >= 0 and value <= 64:
        return 0
    elif value >= 65 and value <= 95:
        return 80
    elif value >= 96 and value <= 126:
        return 100
    elif value >= 127 and value <= 157:
        return 120
    elif value >= 158 and value <= 191:
        return 150
    elif value >= 192 and value <= 232:
        return 210
    else:
        return value

# 提取坐标和像素值
x_values = [int(result[0]) for result in processed_results]
y_values = [int(result[1]) for result in processed_results]
pixel_values = [process_pixel_value(result[4]) for result in processed_results]

# 创建空白图像
image = Image.new("L", (256, 256))

# 根据坐标和像素值填充图像
for x, y, pixel_value in zip(x_values, y_values, pixel_values):
    image.putpixel((int(x), int(y)), int(pixel_value))

# 保存新的图片
image.save("/content/plot.png")

print("新的图片已保存为 plot.png。")

