#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import shutil
import subprocess
from tqdm import tqdm
import os

#image_path = '/content/plot_finished.png'  # 原始图片路径
n = 16  # 循环次数

total_iterations = n * 3  # 总迭代次数，每次循环进行三个操作：复制图片、运行程序和删除文件

with tqdm(total=total_iterations, desc="Progress", unit="iteration") as pbar:
    for i in range(1, n + 1):
        get_ipython().system('python /content/1.py')
        os.remove('/content/plot_finished.png')
        get_ipython().system('python /content/2.py')
        get_ipython().system('python /content/3.py')
        get_ipython().system('python /content/4.py')
        get_ipython().system('python /content/5.py')
        get_ipython().system('python /content/6.py')
        get_ipython().system('python /content/7.py')
        get_ipython().system('python /content/8.py')
        get_ipython().system('python /content/9.py')
        get_ipython().system('python /content/10.py')
        # 删除文件
        
        os.remove('/content/new_array.pkl')
        os.remove('/content/new_image_256.png')
        os.remove('/content/output_256.pkl')
        os.remove('/content/processed_results.pkl')
        os.remove('/content/query_results.pkl')
        os.remove('/content/result_array.pkl')
        os.remove('/content/result_data.pkl')
        os.remove('/content/statistics_results.pkl')
        os.remove('/content/plot.png')
        print("文件删除成功")
        pbar.update(1)  # 更新进度条
        

        
        new_image_path = f'/content/plot_finished{i}.png'  # 新图片路径
        image_path = '/content/plot_finished.png'
        shutil.copyfile(image_path, new_image_path)  # 复制图片文件
        print(f"图片复制成功：{new_image_path}")
        pbar.update(1)  # 更新进度条
        print("程序 未命名2 运行成功")
        pbar.update(1)  # 更新进度条
       
            

