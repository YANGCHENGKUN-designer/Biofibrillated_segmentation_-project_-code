#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PIL import Image

# 读取原始图像
image_path = '/content/plot.png'
original_image = Image.open(image_path)

# 创建新的256x256灰度图像
new_image = Image.new('L', (256, 256))

# 计算缩放比例
width, height = original_image.size
scale = min(256 / width, 256 / height)

# 缩放原始图像并居中放置到新图像中
new_width = int(width * scale)
new_height = int(height * scale)
resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
x_offset = (256 - new_width) // 2
y_offset = (256 - new_height) // 2
new_image.paste(resized_image, (x_offset, y_offset))

# 保存新图像
new_image_path = '/content/plot_finished.png'
new_image.save(new_image_path)


