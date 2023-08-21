#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cv2

# 读取图像
image = cv2.imread('/content/plot.png')

# 转换为灰度图像
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 保存灰度图像，并保持原始尺寸
cv2.imwrite('/content/plot_finished.png', gray_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

print("保存成功！")


# In[ ]:




