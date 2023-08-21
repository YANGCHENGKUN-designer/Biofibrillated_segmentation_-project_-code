#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
from PIL import Image
import numpy as np
import pickle
from tqdm import tqdm

def get_polar_coordinates(image_path, m, n, p):
    # 打开图像
    image = Image.open(image_path)

    # 获取图像尺寸
    width, height = image.size

    # 检查 m 和 n 的范围是否符合条件
    if m <= p or m >= (256 - p) or n <= p or n >= (256 - p):
        polar_coordinates = np.array([(0, 0)])
        cartesian_coordinates = np.array([(m, n)])
        pixel_values = np.array([image.getpixel((m, n))])
    else:
        # 计算图像中心点坐标
        center_x = m
        center_y = n

        # 存储结果
        polar_coordinates = []
        cartesian_coordinates = []
        pixel_values = []
        cartesian_values = []

        # 逐渐变化角度和半径，生成极坐标和直角坐标
        for theta in range(0, 360, 15):
            for r in range(-p, p+1):
                # 将极坐标转换为直角坐标
                x = int(r * math.cos(math.radians(theta)))
                y = int(r * math.sin(math.radians(theta)))

                # 计算图像中心点偏移后的坐标
                pixel_x = center_x + x
                pixel_y = center_y + y

                # 获取像素值
                pixel_value = image.getpixel((pixel_x, pixel_y))

                # 存储结果
                polar_coordinates.append((r, theta))
                cartesian_coordinates.append((pixel_x, pixel_y))
                pixel_values.append(pixel_value)
                cartesian_values.append((x, y))

        # 将结果转换为 NumPy 数组
        polar_coordinates = np.array(polar_coordinates)
        cartesian_coordinates = np.array(cartesian_coordinates)
        pixel_values = np.array(pixel_values)
        cartesian_values = np.array(cartesian_values)

    # 将结果合并为一个数组
    results = np.column_stack((polar_coordinates, pixel_values, cartesian_coordinates))

    return results

def process_results(results):
    theta_values = np.unique(results[:, 1])  # 获取所有不重复的 theta 值

    max_value_theta_i = 0
    new_pixel_value = 0
    x_value = 0
    y_value = 0
    theta_new = 0

    for theta in theta_values:
        # 获取当前 theta 的元素数量和像素值的和
        mask = (results[:, 1] == theta)
        count = np.count_nonzero(mask)
        pixel_sum = np.sum(results[mask][:, 2])
        x_sum = np.sum(results[mask][:, 3])
        y_sum = np.sum(results[mask][:, 4])

        # 更新最大值和新像素值
        if count > 0:
            if pixel_sum > max_value_theta_i:
                max_value_theta_i = pixel_sum
                new_pixel_value = pixel_sum / count
                x_value = x_sum / count
                y_value = y_sum / count
                theta_new = theta

    return max_value_theta_i, new_pixel_value, theta_new, x_value, y_value

coordinates = []
for m in range(0, 256, 1):
    for n in range(0, 256, 1):
        coordinates.append((m, n))

# 示例用法
image_path = '/content/plot_finished.png'
p = 4   # 极坐标半径

# 创建一个列表用于存储结果
results_list = []

# 使用tqdm创建进度条
with tqdm(total=len(coordinates), desc="Processing") as pbar:
    # 遍历每个坐标点
    for idx, coordinate in enumerate(coordinates):
        m = coordinate[0]
        n = coordinate[1]

        # 获取极坐标结果
        results = get_polar_coordinates(image_path, m, n, p)

        # 如果结果有效，则处理结果并存入列表
        if results is not None:
            max_value_theta_i, new_pixel_value, theta_new, x_value, y_value = process_results(results)
            results_list.append([idx+1, theta_new, new_pixel_value, x_value, y_value])
        else:
            # 如果结果无效，填充占位值
            results_list.append([idx+1, None, None, None, None])

        # 更新进度条
        pbar.update(1)

# 保存结果为数据包
with open("/content/output_256.pkl", "wb") as file:
    pickle.dump(results_list, file)

print("结果已保存为 /content/output_256.pkl 数据包。")

