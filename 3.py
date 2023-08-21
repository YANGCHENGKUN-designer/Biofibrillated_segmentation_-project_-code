#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pickle


def generate_rot_o_m_n(m, n):
    if m >= 253 or n >= 253:
        return [(m, abs(n - abs(i))) for i in range(-2, 3)]
    else:
        return [(m, abs(n + i)) for i in range(-2, 3)]


def generate_rot_45_m_n(m, n):
    if m >= 253 or n >= 253:
        return [(abs(m - abs(i)), abs(n - abs(i))) for i in range(-2, 3)]
    else:
        return [(abs(m + i), abs(n + i)) for i in range(-2, 3)]

def generate_rot_90_m_n(m, n):
    if m >= 253 or n >= 253:
        return [(abs(m - abs(i)), n) for i in range(-2, 3)]
    else:
        return [(abs(m + i), n) for i in range(-2, 3)]

def generate_rot_135_m_n(m, n):
    if m >= 253 or n >= 253:
        return [(abs(m - abs(i)), abs(n - abs(i))) for i in range(-2, 3)]
    else:
        return [(abs(m + i), abs(n - i)) for i in range(-2, 3)]

# 构建索引数组
index_array = []
for m in range(256):
    for n in range(256):
        index_array.append((m, n))

# 读取数据
with open('/content/output_256.pkl', 'rb') as f:
    data = pickle.load(f)

# 建立字典
result = {}
for max_value_theta_i, new_pixel_value, theta_new, x_value, y_value in data:
    indices = generate_rot_o_m_n(x_value, y_value)
    outputs = [(new_pixel_value, theta_new) for _ in range(5)]
    for index, output in zip(indices, outputs):
        result[index] = output

# 构建结果数据包
result_data = []
total_indices = len(index_array)

for i, index in enumerate(index_array):
    m, n = index

    # 查询字典
    x_value = m  # 替换为实际的 x 值
    y_value = n  # 替换为实际的 y 值
    index = (x_value, y_value)
    if index in result:
        output = result[index]
        print(f'索引: {index}, 输出值: {output}')
    else:
        print(f'索引: {index} 未找到对应的输出值')


    # 构建每个数据包的格式
    result_row = []




    result_row.append(generate_rot_o_m_n(m, n))



    result_row.append(generate_rot_45_m_n(m, n))

    result_row.append(generate_rot_90_m_n(m, n))

    result_row.append(generate_rot_135_m_n(m, n))

    result_data.append(result_row)

    # 输出进度
    progress = (i + 1) / total_indices * 100
    print("Processing: {:.2f}%".format(progress))

# 保存结果数据包
output_file = "/content/result_data.pkl"
with open(output_file, "wb") as file:
    pickle.dump(result_data, file)

print("结果数据包已保存为 {}".format(output_file))

