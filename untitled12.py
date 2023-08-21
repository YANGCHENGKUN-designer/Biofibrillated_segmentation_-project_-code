# -*- coding: utf-8 -*-
"""Untitled12.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FL8sOE8sXftJvl20VuDYzleulwOPmKvi
"""

import numpy as np
from PIL import Image

# 读取灰度图像
image_path = "/content/plot_finished.png"
image = Image.open(image_path).convert("L")  # 转换为灰度图像（L代表灰度图像模式）

# 将图像数据转换为NumPy数组
data = np.array(image)

# 将大于191的像素值变为0
data[data > 191] = 0

# 计算剩余像素值中的最小5%值
non_zero_pixels = data[data != 0]  # 剔除为0的像素点
min_5_percent = np.percentile(non_zero_pixels, 5)

# 将小于最小5%值的像素点设置为0
data[data < min_5_percent] = 0

# 将处理后的数组转换回图像
processed_image = Image.fromarray(data)

# 保存处理后的图像
processed_image_path = "/content/processed_plot.png"
processed_image.save(processed_image_path)

# 显示处理后的图像
processed_image.show()



# -*- coding: utf-8 -*-
"""83heshi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-I_Eud962ANR-rF-a16-8kX4apjFDv_z
"""

#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import shutil
import numpy as np
from PIL import Image
import cv2
from google.colab.patches import cv2_imshow
import json
import re
import matplotlib.pyplot as plt
import os
import random

# In[ ]:


def read_image_and_get_info(image_path):
    try:
        # 读取图片
        image = Image.open(image_path)
        # 获取图片大小（宽度和高度）
        width, height = image.size
        # 获取图片像素点
        pixels = list(image.getdata())
        # 将像素点转换为字典格式
        pixel_dict = {}
        for x in range(width):
            for y in range(height):
                pixel_value = pixels[y * width + x]
                pixel_dict[(x, y)] = pixel_value

        return pixel_dict
    except Exception as e:
        print("Error:", e)
        return None

def get_top_1_by_256_pixels(pixel_dict):
    sorted_pixels = sorted(pixel_dict.items(), key=lambda x: x[1], reverse=True)
    num_top_pixels = len(sorted_pixels) // 256
    top_pixel_points = {point: pixel_value for point, pixel_value in sorted_pixels[:num_top_pixels]}

    middle_pixel_index = len(sorted_pixels) // 2
    middle_pixel_points = {point: pixel_value for point, pixel_value in sorted_pixels[middle_pixel_index:middle_pixel_index+num_top_pixels]}

    bottom_pixel_points = {point: pixel_value for point, pixel_value in sorted_pixels[-num_top_pixels:]}

    # Combine all three dictionaries into a single dictionary
    top_pixel_points.update(middle_pixel_points)
    top_pixel_points.update(bottom_pixel_points)

    return top_pixel_points

def get_random_64_points():
    points = []
    for x in range(0, 256, 64):
        for y in range(0, 256, 64):
            max_pixel_value = 0
            max_pixel_point = None
            for i in range(64):
                for j in range(64):
                    pixel_point = (x + i, y + j)
                    pixel_value = pixel_dict.get(pixel_point, 0)
                    if pixel_value > max_pixel_value:
                        max_pixel_value = pixel_value
                        max_pixel_point = pixel_point
                    elif pixel_value == max_pixel_value:
                        # Randomly choose one if multiple points have the same max pixel value
                        if random.random() < 0.5:
                            max_pixel_point = pixel_point
            points.append(max_pixel_point)
    return points

def save_points_to_txt(points, file_path):
    with open(file_path, 'w') as f:
        for point in points:
            f.write(f"{point[0]}, {point[1]}, {pixel_dict.get(point, 0)}\n")



def bilateral_filter(input_image, diameter, spatial_sigma):
    # 对输入灰度图像应用双边滤波
    filtered_image = cv2.bilateralFilter(input_image, diameter, 0, spatial_sigma)
    return filtered_image

def block_bilateral_filter(input_image, diameter, spatial_sigma, block_size=100):
    # 获取图像的尺寸
    h, w = input_image.shape

    # 创建一个空白图像用于存储滤波后的结果
    filtered_image = input_image.copy()

    # 对图像进行分块处理并应用双边滤波
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            block = input_image[y:y + block_size, x:x + block_size]
            filtered_block = bilateral_filter(block, diameter, spatial_sigma)
            filtered_image[y:y + block_size, x:x + block_size] = filtered_block

    return filtered_image

def sobel_gradients(image):
    # 将输入图像转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用Sobel算子计算梯度gx和gy
    gx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)

    # 计算梯度幅值和方向
    gradient_magnitude = np.sqrt(gx**2 + gy**2)
    gradient_angle = np.arctan2(gy, gx)

    return gx, gy, gradient_magnitude, gradient_angle, gray_image


def compute_gradients(gradient_info_dict, x, y):
    if x == 0 or y == 0 or x == 255 or y == 255:
        # If x or y is 0 or 255, directly set thea to 0
        return 0, 0, 0

    # Get gx and gy values for the given coordinate (x, y) from the dictionary
    key = f"({x}, {y})"
    gx = gradient_info_dict[key][0]
    gy = gradient_info_dict[key][1]

    # Save Gx and Gy values for the surrounding 9 points (including itself)
    Gx_points = []
    Gy_points = []

    # Loop through the surrounding 9 points (3x3 neighborhood)
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if 1 <= i <= 254 and 1 <= j <= 254:  # Check if the point is within image boundaries
                # Get gx and gy values for the surrounding point (i, j) from the dictionary
                key = f"({i}, {j})"
                gx = gradient_info_dict[key][0]
                gy = gradient_info_dict[key][1]

                # Save the Gx and Gy values for the surrounding point (i, j)
                Gx_points.append(gx)
                Gy_points.append(gy)

    # Calculate g_sx_result and g_sy_result
    g_sx_result = sum(Gx_points)
    g_sy_result = sum(Gy_points)

    # Calculate thea, handling ZeroDivisionError
    if g_sx_result == 0:
        thea = 0  # Set thea to 0 when g_sx_result is 0
    else:
        value = g_sy_result / g_sx_result
        thea = np.arctan(value) / 2 + np.pi / 2

    return g_sx_result, g_sy_result, thea


def query_result(x, y):
    # Convert x and y to integers
    x, y = int(x), int(y)

    # Check if (x, y) is a valid coordinate in the results_dict
    key = f"{x},{y}"
    if key not in results_dict_loaded:
        return None

    # Create a 3x3 array to store the thea values for the neighborhood
    thea_array = np.empty((3, 3), dtype=float)

    # Handle special cases when x or y is 0 or 255
    if x == 0 or x == 255 or y == 0 or y == 255:
        thea_value = results_dict_loaded[key][2]  # Get the thea value for the (x, y) coordinate
        thea_array.fill(thea_value)  # Fill the entire 3x3 array with the same thea value
    else:
        # Traverse the 3x3 neighborhood and get the thea values
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                # Get the key for the current (i, j) coordinate
                current_key = f"{i},{j}"

                # Check if the current coordinate is available in the results_dict
                if current_key in results_dict_loaded:
                    # Get the thea value for the current (i, j) coordinate
                    thea_value = results_dict_loaded[current_key][2]
                else:
                    # If the current coordinate is not available, set the thea value to 0
                    thea_value = 0.0

                # Store the thea value in the thea_array
                thea_array[i-x+1, j-y+1] = thea_value

    return thea_array


def calculate_coherence(thea_array):
    # Extract the middle value from thea_array
    value_middle = thea_array[1, 1]

    # Subtract value_middle from each element of thea_array
    thea_array_process = value_middle - thea_array

    # Calculate cos values for each element of thea_array_process
    cos_values = np.cos(thea_array_process)

    # Calculate coherence by summing up the cos values and dividing by 9
    coherence = np.sum(cos_values) / 9

    return coherence

def query_values(x, y):
    # Convert x and y to integers
    x, y = int(x), int(y)

    # Query coherence value from coherence_dict
    coherence_value = coherence_dict.get((x, y), None)

    # Query thea value from results_dict
    thea_value = results_dict.get(f"{x},{y}", [None, None, None])[2]

    return coherence_value, thea_value


def read_seed_points_from_file(file_path):
    # Read seed points from the file and return as a list of (x, y) tuples
    seed_points = []
    with open(file_path, 'r') as file:
        for line in file:
            # Use regular expressions to extract integers from each line
            matches = re.findall(r'\d+', line)
            if len(matches) >= 2:
                x, y = map(int, matches[:2])
                seed_points.append((x, y))
    return seed_points

def region_growing(image, seed_points, threshold, coherence_dict, thea_dict):
    h, w = image.shape[:2]
    visited = np.zeros((h, w), dtype=np.bool)
    region = np.zeros_like(image, dtype=np.uint8)

    for seed_point in seed_points:
        x, y = seed_point
        seed_value = image[x, y]
        seed_orientation = thea_dict[seed_point]
        seed_coherence = coherence_dict[seed_point]
        seed_queue = [(x, y)]

        orientation_similarity = pixel_similarity = coherence_similarity = 1.0

        while seed_queue:
            x, y = seed_queue.pop()
            if not visited[x, y]:
                visited[x, y] = True

                # Check the pixel similarity with the seed point
                pixel_difference = abs(image[x, y] - seed_value)
                if pixel_difference <= threshold:
                    region[x, y] = 255

                    # Check nearby 8 points for orientation, pixel, and coherence values
                    orientation_probs = []
                    pixel_probs = []
                    coherence_probs = []

                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (0 <= x + i < h) and (0 <= y + j < w) and not visited[x + i, y + j]:
                                orientation_difference = abs(thea_dict[(x + i, y + j)] - seed_orientation)
                                pixel_difference = abs(image[x + i, y + j] - image[seed_point])
                                coherence_difference = abs(coherence_dict[(x + i, y + j)] - seed_coherence)

                                # Calculate probabilities
                                orientation_prob = max(0.3, 1.0 - orientation_difference * 0.1)
                                pixel_prob = max(0.3, 1.0 - pixel_difference * 0.1)
                                coherence_prob = max(0.3, 1.0 - coherence_difference * 0.1)

                                orientation_probs.append(orientation_prob)
                                pixel_probs.append(pixel_prob)
                                coherence_probs.append(coherence_prob)

                                # Update similarities
                                orientation_similarity *= orientation_prob
                                pixel_similarity *= pixel_prob
                                coherence_similarity *= coherence_prob

                                seed_queue.append((x + i, y + j))

        # Take 8 directions' maximum probability value if orientation_probs is not empty
        if orientation_probs:
            max_prob_index = np.argmax(orientation_probs)
            max_prob_direction = [(x + i, y + j) for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]][max_prob_index]
            max_prob_value = orientation_probs[max_prob_index] * pixel_probs[max_prob_index]

            # If the maximum probability direction exists, add to the seed queue
            if max_prob_value > 0.5 * 0.5 * 0.5:  # Adjusting similarity threshold
                seed_queue.append(max_prob_direction)
                region[x, y] = 255
        else:
            # Handle the case when there are no valid neighbors
            # For example, mark the current pixel as visited
            visited[x, y] = True

    return region, orientation_similarity, pixel_similarity, coherence_similarity

def main():
    # Read the image in grayscale
    image = cv2.imread('/content/plot_finished.png', cv2.IMREAD_GRAYSCALE)

    # Load parameter information (orientation)
    thea_dict = np.load('/content/thea_dict.npy', allow_pickle=True).item()

    # Load coherence information (you may need to adjust the path)
    coherence_dict = np.load('/content/coherence_dict.npy', allow_pickle=True).item()

    # Define seed points (you can read them from a file or specify them manually)
    seed_points = read_seed_points_from_file('/content/top_pixel_points.txt')

    # Set the similarity threshold (you may need to adjust this based on your image and application)
    threshold = 30

    # Perform region growing segmentation
    segmented_region, _, _, _ = region_growing(image, seed_points, threshold, coherence_dict, thea_dict)

    # Display the segmented region using matplotlib
    plt.imshow(segmented_region, cmap='gray')
    plt.title('Segmented Region')
    plt.axis('off')
    plt.show()

    # Save the segmented image
    cv2.imwrite('/content/segmented_image.png', segmented_region)

def read_grayscale_images(filepath1, filepath2):
    try:
        image1 = Image.open(filepath1)
        image2 = Image.open(filepath2)

        if image1.mode != 'L' or image2.mode != 'L':
            raise ValueError("Both images should be in grayscale mode (L mode).")

        width1, height1 = image1.size
        width2, height2 = image2.size
        max_width = max(width1, width2)
        max_height = max(height1, height2)

        pixel_values = []
        for y in range(max_height):
            for x in range(max_width):
                pixel_value1 = image1.getpixel((x, y)) if x < width1 and y < height1 else None
                pixel_value2 = image2.getpixel((x, y)) if x < width2 and y < height2 else None
                pixel_values.append((x, y, pixel_value1, pixel_value2))

        return pixel_values

    except IOError as e:
        print(f"Error while reading the images: {e}")
        return None


def calculate_t_from_array(array_filepath,c):
    try:
        data_array = np.loadtxt(array_filepath, delimiter=',', skiprows=1)
        image1_pixel_values = data_array[:, 2]  # Get the Image1 Pixel Values from the array

        # Sort the Image1 Pixel Values in ascending order
        sorted_pixel_values = np.sort(image1_pixel_values)

        # Calculate the index for the 20th percentile
        percentile_index = int(len(sorted_pixel_values) * c)

        # Get the 20% smallest values
        smallest_20_percent = sorted_pixel_values[:percentile_index]

        # Find the maximum value from the smallest 20%
        t = np.max(smallest_20_percent)

        return t

    except IOError as e:
        print(f"Error while reading the array file: {e}")
        return None


def process_array(array_filepath, t):
    try:
        data_array = np.loadtxt(array_filepath, delimiter=',', skiprows=1)
        image1_pixel_values = data_array[:, 2]  # Get the Image1 Pixel Values from the array
        image2_pixel_values = data_array[:, 3]  # Get the Image2 Pixel Values from the array

        # Iterate through the array and process the values
        for i in range(len(data_array)):
            if image2_pixel_values[i] == 0:
                if image1_pixel_values[i] < t:
                    data_array[i, 2] = 0  # Set Image1 Pixel Value to 0
            # If image2_pixel_values[i] is not 0, no changes needed for Image1 Pixel Value

        # Save the processed array to a new file
        processed_filepath = "processed_output_array.txt"
        np.savetxt(processed_filepath, data_array, fmt='%d', delimiter=',', header='x, y, Image1 Pixel Value, Image2 Pixel Value', comments='')
        print(f"Processed array saved as {processed_filepath}")

    except IOError as e:
        print(f"Error while reading the array file: {e}")


def calculate_p_from_array(array_filepath,c):
    try:
        data_array = np.loadtxt(array_filepath, delimiter=',', skiprows=1)
        image1_pixel_values = data_array[:, 2]  # Get the Image1 Pixel Values from the array

        # Sort the Image1 Pixel Values in descending order
        sorted_pixel_values = np.sort(image1_pixel_values)[::-1]

        # Calculate the index for the 20th percentile
        percentile_index = int(len(sorted_pixel_values) * c)

        # Get the 20% largest values
        largest_20_percent = sorted_pixel_values[:percentile_index]

        # Find the minimum value from the largest 20%
        p = np.min(largest_20_percent)

        return p

    except IOError as e:
        print(f"Error while reading the array file: {e}")
        return None

def process_array_finished(array_filepath, p):
    try:
        data_array = np.loadtxt(array_filepath, delimiter=',', skiprows=1)
        image1_pixel_values = data_array[:, 2]  # Get the Image1 Pixel Values from the array
        image2_pixel_values = data_array[:, 3]  # Get the Image2 Pixel Values from the array

        # Iterate through the array and process the values
        for i in range(len(data_array)):
            if image2_pixel_values[i] == 255:
                if image1_pixel_values[i] > p:
                    data_array[i, 2] = 255  # Set Image1 Pixel Value to 255
            # If image2_pixel_values[i] is not 255, no changes needed for Image1 Pixel Value

        # Save the processed array to a new file
        processed_filepath = "processed_output_array_finished.txt"
        np.savetxt(processed_filepath, data_array, fmt='%d', delimiter=',', header='x, y, Image1 Pixel Value, Image2 Pixel Value', comments='')
        print(f"Processed array saved as {processed_filepath}")

    except IOError as e:
        print(f"Error while reading the array file: {e}")



def plot_image_from_array(processed_array):
    x_coords = processed_array[:, 0]
    y_coords = processed_array[:, 1]
    image1_pixel_values = processed_array[:, 2]

    width = int(np.max(x_coords)) + 1
    height = int(np.max(y_coords)) + 1

    image1_matrix = np.zeros((height, width), dtype=np.uint8)

    for i in range(len(x_coords)):
        x = int(x_coords[i])
        y = int(y_coords[i])
        pixel_value = int(image1_pixel_values[i])
        image1_matrix[y, x] = pixel_value

    plt.imshow(image1_matrix, cmap='gray')
    plt.axis('off')
    plt.show()


# In[ ]:


if __name__ == "__main__":
    c_value = 0.1
    for i in range(60):  # 60 cycles, can also be adjusted as needed
        # Source file path
        source_file_path = "/content/plot_finished.png"
        # Get the directory where the source file is located
        directory = os.path.dirname(source_file_path)
        # Copy the file and save it
        copy_file_name = f"plot_finished_a_{i}.png"
        copy_file_path = os.path.join(directory, copy_file_name)
        shutil.copy(source_file_path, copy_file_path)
        print(f"The file has been copied as {copy_file_name}")
        if c_value < 0.20:
            c_value += 0.001
        elif 0.20 <= c_value < 0.3:
            c_value += 0.0005
        elif 0.3 <= c_value < 0.4:
            c_value += 0.001
        else:
            c_value = 0.45

        print("当前c_value值：", c_value)
        # 在这里添加你想要运行的小程序代码
        c = c_value
        image_path = "/content/plot_finished.png"
        pixel_dict = read_image_and_get_info(image_path)

        if pixel_dict:
            # 输出像素值
            for (x, y), pixel_value in pixel_dict.items():
                print(f"坐标点 ({x}, {y}) 像素值：{pixel_value}")

            # 将结果保存为.npy文件
            np.save("/content/pixel_values.npy", pixel_dict)
        else:
            print("无法读取图片信息。")



        # 读取.npy文件
        pixel_dict = np.load("/content/pixel_values.npy", allow_pickle=True).item()

        # 获取前1/256的像素值及其坐标点
        top_pixel_points = get_top_1_by_256_pixels(pixel_dict)

        # 获取64个随机点
        random_64_points = get_random_64_points()

        # 将结果保存为.txt文件
        save_points_to_txt(list(top_pixel_points.keys()) + random_64_points, "/content/top_pixel_points.txt")





        # 加载输入灰度图像
        input_image = cv2.imread("/content/plot_finished.png", cv2.IMREAD_GRAYSCALE)

        # 设置双边滤波的参数
        diameter = 6 # Diameter of each pixel neighborhood (larger values smooth more)
        spatial_sigma = 16  # Filter sigma in the coordinate space (larger value means pixels farther apart will influence more)

        # 应用分块双边滤波
        filtered_image = block_bilateral_filter(input_image, diameter, spatial_sigma)

        # 使用 cv2_imshow 显示原始图像和滤波后的图像
        cv2_imshow(input_image)
        cv2_imshow(filtered_image)

        # 保存处理后的图像
        cv2.imwrite("/content/Noise_finished.png", filtered_image)

        # 等待按键按下后关闭所有窗口
        cv2.waitKey(0)
        cv2.destroyAllWindows()



        # 加载指定路径的图像
        image_path = '/content/Noise_finished.png'
        image = cv2.imread(image_path)

        # 获取梯度gx、gy、幅值、方向和灰度图像
        gx, gy, gradient_magnitude, gradient_angle, gray_image = sobel_gradients(image)

        # 将像素点的坐标位置、gx、gy、幅值大小、方向大小和像素值保存为一个字典
        gradient_info_dict = {}
        rows, cols = gradient_magnitude.shape
        for r in range(rows):
            for c in range(cols):
                # 获取像素点的坐标位置、gx、gy、幅值大小、方向大小和像素值
                x = c
                y = r
                gx_val = float(gx[r, c])
                gy_val = float(gy[r, c])
                magnitude = float(gradient_magnitude[r, c])
                angle = float(gradient_angle[r, c])
                pixel_value = int(gray_image[r, c])

                # 构建索引对应的数组
                索引数组 = [gx_val, gy_val, magnitude, angle, pixel_value]

                # 将信息添加到字典中，并将坐标位置 (x, y) 转换为字符串作为键
                gradient_info_dict[str((x, y))] = 索引数组

        # 将字典保存为json文件
        with open('/content/gradient_info_dict.json', 'w') as f:
            json.dump(gradient_info_dict, f)

        # 输出保存成功
        print("字典已保存为gradient_info_dict.json文件！")






            # Load the gradient information dictionary from the JSON file
        with open('/content/gradient_info_dict.json', 'r') as f:
            gradient_info_dict = json.load(f)

        # Create a new dictionary to store the results
        results_dict = {}

        # Traverse all points from (0, 0) to (255, 255)
        for x in range(256):
            for y in range(256):
                g_sx_result, g_sy_result, thea = compute_gradients(gradient_info_dict, x, y)
                results_dict[f"{x},{y}"] = [g_sx_result, g_sy_result, thea]

        # Save the results dictionary to a numpy file
        np.save('/content/results_dict.npy', results_dict)

        # Load the results dictionary from the numpy file
        results_dict_loaded = np.load('/content/results_dict.npy', allow_pickle=True).item()

        # Print the results
        for key, result in results_dict_loaded.items():
            x, y = map(int, key.split(','))
            print("x:", x, "y:", y, "result:", result)


            # Load the results dictionary from the numpy file
        results_dict_loaded = np.load('/content/results_dict.npy', allow_pickle=True).item()


        # Create a dictionary to store the results
        coherence_dict = {}


            # Loop through all (x, y) coordinates from (0, 0) to (255, 255)
        for x in range(256):
            for y in range(256):
                thea_array = query_result(x, y)
                if thea_array is not None:
                    coherence = calculate_coherence(thea_array)
                    coherence_dict[(x, y)] = coherence

        # Print the results
        for (x, y), coherence in coherence_dict.items():
            print(f"Coordinate (x={x}, y={y}), Coherence: {coherence}")

        # Save the coherence dictionary to a .npy file
        np.save('/content/coherence_dict.npy', coherence_dict)

        # Print the results (optional, you can remove this part if not needed)
        for (x, y), coherence in coherence_dict.items():
            print(f"Coordinate (x={x}, y={y}), Coherence: {coherence}")



        # Load the coherence_dict and results_dict dictionaries from the .npy files
        coherence_dict = np.load('/content/coherence_dict.npy', allow_pickle=True).item()
        results_dict = np.load('/content/results_dict.npy', allow_pickle=True).item()


        # Create a new dictionary to store the results
        c_thea_finished = {}
        # Loop through all (x, y) coordinates from (0, 0) to (255, 255)
        for x in range(256):
            for y in range(256):
                # Query the coherence and thea values for the current coordinates
                coherence, thea = query_values(x, y)

                # Store the results in the new dictionary
                c_thea_finished[(x, y)] = [coherence, thea]

        # Save the new dictionary as .npy file
        np.save('/content/c_thea_finished.npy', c_thea_finished)

        # Print the saved dictionary
        print(np.load('/content/c_thea_finished.npy', allow_pickle=True).item())

        # 读取.npy文件，获取字典
        data = np.load('/content/c_thea_finished.npy', allow_pickle=True).item()
        # 遍历x和y，并获取索引和thea值，保存结果到列表
        thea_values = []
        for x in range(256):
            for y in range(256):
                index = (x, y)
                if index in data:
                    thea_value = data[index][1]  # 获取thea值
                    thea_values.append((x, y, thea_value))

        # 将结果保存到txt文件
        output_file = "thea_values.txt"
        with open(output_file, "w") as file:
            for item in thea_values:
                file.write(f"{item[0]}, {item[1]}, {item[2]}\n")

        print("保存成功！")


        thea_values = []
        coordinates = []  # To store the (x, y) coordinates

        with open('/content/thea_values.txt', 'r') as f:
            for line in f:
                x, y, thea = map(float, line.strip().split(','))
                thea_values.append(thea)
                coordinates.append((int(x), int(y)))  # Save the (x, y) coordinates

        # Process thea values (subtract -pi/2 and convert to degrees)
        processed_thea_values = [np.degrees(thea - np.pi/2) for thea in thea_values]

        # Create a dictionary with (x, y) as keys and processed_thea_values as values
        thea_dict = {}
        for coord, thea_value in zip(coordinates, processed_thea_values):
            x, y = coord
            thea_dict[(x, y)] = thea_value

        # Save the thea_dict as .npy file
        np.save('/content/thea_dict.npy', thea_dict)






        main()




        image_filepath1 = "/content/plot_finished.png"
        image_filepath2 = "/content/segmented_image.png"
        pixels = read_grayscale_images(image_filepath1, image_filepath2)

        if pixels:
            data_array = np.array(pixels)
            np.savetxt("output_array.txt", data_array, fmt='%d', delimiter=',', header='x, y, Image1 Pixel Value, Image2 Pixel Value', comments='')
            print("Result saved as output_array.txt")



        array_filepath = "output_array.txt"
        c= c_value
        t_value = calculate_t_from_array(array_filepath,c)
        if t_value is not None:
            print(f"The value of t is: {t_value}")





        array_filepath = "output_array.txt"
        c= c_value
        t_value = calculate_t_from_array(array_filepath,c)
        if t_value is not None:
            print(f"The value of t is: {t_value}")
            process_array(array_filepath, t_value)



        array_filepath = "processed_output_array.txt"
        c= c_value
        p_value = calculate_p_from_array(array_filepath,c)
        if p_value is not None:
            print(f"The value of p is: {p_value}")
            process_array_finished(array_filepath, p_value)


        processed_array_filepath = "/content/processed_output_array_finished.txt"
        processed_array = np.loadtxt(processed_array_filepath, delimiter=',', skiprows=1)

        plot_image_from_array(processed_array)



        # 读取数据文件，并指定逗号为分隔符，只读取前三列数据
        data_file = "/content/processed_output_array_finished.txt"
        data = np.loadtxt(data_file, delimiter=',', usecols=(0, 1, 2), skiprows=1)

        # 提取x_coords、y_coords和image1_pixel_values数据
        x_coords = data[:, 0]
        y_coords = data[:, 1]
        image1_pixel_values = data[:, 2]

        # 创建一个空白的256x256图像矩阵
        image_size = 256
        image = np.zeros((image_size, image_size))

        # 遍历x_coords和y_coords数组，并将对应的像素值填充到图像矩阵中
        for x, y, pixel_value in zip(x_coords, y_coords, image1_pixel_values):
            image[int(y), int(x)] = pixel_value

        # 现在image矩阵中存储了图像的灰度值

        # 将图像矩阵转换为PIL图像对象
        image = Image.fromarray(image.astype(np.uint8))

        # 保存图像为PNG文件
        output_file = "/content/output_image.png"
        image.save(output_file)

        # 打印成功信息
        print(f"图像已生成并保存为{output_file}")

        # 源文件路径
        source_file_path = "/content/output_image.png"

        # 目标文件名
        target_file_name = "plot_finished.png"

        # 获取源文件所在的目录
        directory = os.path.dirname(source_file_path)

        # 拼接目标文件的完整路径
        target_file_path = os.path.join(directory, target_file_name)

        # 重命名文件
        os.rename(source_file_path, target_file_path)

        print(f"文件已重命名为 {target_file_name}")











import cv2

def extract_center(image_path, target_size=256, output_path="center_image.png"):
    # 读取灰度图像
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 获取图像尺寸
    height, width = gray_image.shape

    # 计算中心区域的起始坐标
    start_x = max(0, (width - target_size) // 2)
    start_y = max(0, (height - target_size) // 2)

    # 提取中心区域
    center_image = gray_image[start_y:start_y + target_size, start_x:start_x + target_size]

    # 保存提取的中心区域图片
    cv2.imwrite(output_path, center_image)

if __name__ == "__main__":
    # 图像文件路径
    input_image_path = "/content/KO_1_gen.png"

    # 提取中心区域，并保存输出的图片
    output_image_path = "center_image.png"
    extract_center(input_image_path, output_path=output_image_path)

    print("中心区域图片已保存为:", output_image_path)

