#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle

# 读取数据
with open('/content/output_256.pkl', 'rb') as f:
    data = pickle.load(f)

# 建立字典
result = {}
for max_value_theta_i, new_pixel_value, theta_new, x_value, y_value in data:
    index = (x_value, y_value)
    output = (new_pixel_value, theta_new)
    result[index] = output

# 打印结果
for index, output in result.items():
    print(f'索引: {index}, 输出值: {output}')

import pickle

# 加载.pkl文件
with open('/content/result_data.pkl', 'rb') as f:
    data = pickle.load(f)

# 遍历坐标值并输出为数组
result_array = []
for array in data:
    for coordinates in array:
        for (m, n) in coordinates:
            result_array.append((m, n))

# 打印结果数组
print(result_array)

# 保存为数据包
with open('/content/result_array.pkl', 'wb') as f:
    pickle.dump(result_array, f)

print("保存成功！")

