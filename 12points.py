# -*- coding: utf-8 -*-
"""12points.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nIPXkoT1ZDPg_wKsYiIlw4LI_vCjFi0h
"""

import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 读取数据
data = np.loadtxt('/content/cluster_145.txt')  # 替换为实际文件路径

# 提取X和Y坐标
X = data[:, 0].reshape(-1, 1)
Y = data[:, 1].reshape(-1, 1)

# 使用谱聚类算法将坐标点分类
n_clusters = 2 # 设置要分类的簇数，根据数据情况进行调整
model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
cluster_labels = model.fit_predict(data)

# 绘制聚类结果
plt.scatter(X, Y, c=cluster_labels, cmap='rainbow')
plt.title('Spectral Clustering')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# 定义多条曲线拟合函数
def multi_curve_fit(x, *params):
    num_curves = len(params) // 3
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c = params[i * 3:i * 3 + 3]
        y_fit += a * np.sin(b * x) + c
    return y_fit

# 提取簇的数据并拟合多条曲线
for cluster_num in range(n_clusters):
    cluster_data = data[cluster_labels == cluster_num]
    if len(cluster_data) > 0:
        x_fit = cluster_data[:, 0]
        y_fit = cluster_data[:, 1]

        # 使用曲线拟合函数进行非线性拟合
        num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
        initial_params = [1.0, 1.0, 1.0] * num_curves
        popt, _ = curve_fit(multi_curve_fit, x_fit, y_fit, p0=initial_params)

        # 绘制拟合曲线
        x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
        y_curve = multi_curve_fit(x_curve, *popt)
        plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num}')
        plt.scatter(x_fit, y_fit, marker='x')

plt.title('Curve Fitting')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

import numpy as np
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt

# 读取数据
data = np.loadtxt('/content/processed_non_black_pixels-2.txt')  # 替换为实际文件路径

# 提取X和Y坐标
X = data[:, 0].reshape(-1, 1)
Y = data[:, 1].reshape(-1, 1)

# 使用谱聚类算法将坐标点分类
n_clusters = 150 # 设置要分类的簇数，根据数据情况进行调整
model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
cluster_labels = model.fit_predict(data)

# 绘制聚类结果
plt.scatter(X, Y, c=cluster_labels, cmap='rainbow')
plt.title('Spectral Clustering')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()



import numpy as np
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt

# 读取数据
data = np.loadtxt('/content/processed_non_black_pixels-2.txt')  # 替换为实际文件路径

# 提取X和Y坐标
X = data[:, 0].reshape(-1, 1)
Y = data[:, 1].reshape(-1, 1)

# 使用谱聚类算法将坐标点分类
n_clusters = 150  # 设置要分类的簇数，根据数据情况进行调整
model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
cluster_labels = model.fit_predict(data)

# 绘制聚类结果
plt.scatter(X, Y, c=cluster_labels, cmap='rainbow')
plt.title('Spectral Clustering')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# 保存聚类结果
for i in range(n_clusters):
    cluster_i_indices = np.where(cluster_labels == i)[0]
    cluster_i_data = data[cluster_i_indices].astype(int)
    np.savetxt(f"/content/cluster_{i}.txt", cluster_i_data, fmt='%d')



import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义多条3阶多项式拟合函数
def poly_fit_func(x, *params):
    num_curves = len(params) // 4
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c, d = params[i * 4:i * 4 + 4]
        y_fit += a * x**3 + b * x**2 + c * x + d
    return y_fit

# 定义执行谱聚类和拟合的函数
def cluster_and_fit(filename):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 1  # 设置要分类的簇数，根据数据情况进行调整
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
    cluster_labels = model.fit_predict(data)

    # 绘制聚类结果
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow')
    plt.title('Spectral Clustering')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    # 提取簇的数据并进行多条3阶多项式拟合
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用多条3阶多项式拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(poly_fit_func, x_fit, y_fit, p0=initial_params)

            # 绘制拟合曲线
            x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
            y_curve = poly_fit_func(x_curve, *popt)
            plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num}')
            plt.scatter(x_fit, y_fit, marker='x')

    plt.title('Polynomial Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 4):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_5.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename)

import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义多条3阶多项式拟合函数
def poly_fit_func(x, *params):
    num_curves = len(params) // 4
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c, d = params[i * 4:i * 4 + 4]
        y_fit += a * x**3 + b * x**2 + c * x + d
    return y_fit

# 定义执行谱聚类和拟合的函数
def cluster_and_fit(filename):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 1  # 设置要分类的簇数，根据数据情况进行调整
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
    cluster_labels = model.fit_predict(data)

    # 绘制聚类结果
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow')
    plt.title('Spectral Clustering')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show()

    # 提取簇的数据并进行多条3阶多项式拟合
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用多条3阶多项式拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(poly_fit_func, x_fit, y_fit, p0=initial_params)

            # 绘制拟合曲线
            x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
            y_curve = poly_fit_func(x_curve, *popt)
            plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num}')
            plt.scatter(x_fit, y_fit, marker='x')

            # 打印拟合曲线方程式
            equation_str = f'Cluster {cluster_num} Equation: '
            for i in range(num_curves):
                a, b, c, d = popt[i * 4:i * 4 + 4]
                equation_str += f'{a:.2f}x^3 + {b:.2f}x^2 + {c:.2f}x + {d:.2f}   '
            print(equation_str)

    plt.title('Polynomial Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 4):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_5.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename)

import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义多条3阶多项式拟合函数
def poly_fit_func(x, *params):
    num_curves = len(params) // 4
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c, d = params[i * 4:i * 4 + 4]
        y_fit += a * x**3 + b * x**2 + c * x + d
    return y_fit

# 定义执行谱聚类和拟合的函数
def cluster_and_fit(filename):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 1  # 设置要分类的簇数，根据数据情况进行调整
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
    cluster_labels = model.fit_predict(data)

    # 提取簇的数据并进行多条3阶多项式拟合
    fitted_curves = {}  # 用于保存每个簇的拟合曲线方程式和数据
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用多条3阶多项式拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(poly_fit_func, x_fit, y_fit, p0=initial_params)

            # 保存拟合曲线方程式和数据到字典
            fitted_curves[cluster_num] = {
                'equation': popt,
                'data': cluster_data
            }

    # 绘制聚类结果和所有拟合曲线
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow', label='Original Data')
    for cluster_num, curve_data in fitted_curves.items():
        x_fit = curve_data['data'][:, 0]
        y_fit = curve_data['data'][:, 1]
        popt = curve_data['equation']

        # 绘制拟合曲线
        x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
        y_curve = poly_fit_func(x_curve, *popt)
        plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num} Curve')

    plt.title('Polynomial Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 4):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_5.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义多条3阶多项式拟合函数
def poly_fit_func(x, *params):
    num_curves = len(params) // 4
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c, d = params[i * 4:i * 4 + 4]
        y_fit += a * x**3 + b * x**2 + c * x + d
    return y_fit

# 定义执行谱聚类和拟合的函数
def cluster_and_fit(filename):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 1  # 设置要分类的簇数，根据数据情况进行调整
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
    cluster_labels = model.fit_predict(data)

    # 提取簇的数据并进行多条3阶多项式拟合
    fitted_curves = {}  # 用于保存每个簇的拟合曲线方程式和数据
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用多条3阶多项式拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(poly_fit_func, x_fit, y_fit, p0=initial_params)

            # 保存拟合曲线方程式和数据到字典
            fitted_curves[cluster_num] = {
                'equation': popt,
                'data': cluster_data
            }

    # 绘制聚类结果和所有拟合曲线
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow', label='Original Data')
    for cluster_num, curve_data in fitted_curves.items():
        x_fit = curve_data['data'][:, 0]
        y_fit = curve_data['data'][:, 1]
        popt = curve_data['equation']

        # 绘制拟合曲线
        x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
        y_curve = poly_fit_func(x_curve, *popt)
        plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num} Curve')

        # 打印拟合曲线方程式
        equation_str = f'Cluster {cluster_num} Equation: '
        for i in range(num_curves):
            a, b, c, d = popt[i * 4:i * 4 + 4]
            equation_str += f'{a:.2f}x^3 + {b:.2f}x^2 + {c:.2f}x + {d:.2f}   '
        print(equation_str)

    plt.title('Polynomial Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 4):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_5.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename)

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义多条3阶多项式拟合函数
def poly_fit_func(x, *params):
    num_curves = len(params) // 4
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c, d = params[i * 4:i * 4 + 4]
        y_fit += a * x**3 + b * x**2 + c * x + d
    return y_fit

# 定义执行谱聚类和拟合的函数
def cluster_and_fit(filename):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 1  # 设置要分类的簇数，根据数据情况进行调整
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
    cluster_labels = model.fit_predict(data)

    # 提取簇的数据并进行多条3阶多项式拟合
    fitted_curves = {}  # 用于保存每个簇的拟合曲线方程式和数据
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用多条3阶多项式拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(poly_fit_func, x_fit, y_fit, p0=initial_params)

            # 保存拟合曲线方程式和数据到字典
            fitted_curves[cluster_num] = {
                'equation': popt,
                'data': cluster_data
            }

    # 绘制聚类结果和所有拟合曲线
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow', label='Original Data')
    for cluster_num, curve_data in fitted_curves.items():
        x_fit = curve_data['data'][:, 0]
        y_fit = curve_data['data'][:, 1]
        popt = curve_data['equation']

        # 绘制拟合曲线
        x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
        y_curve = poly_fit_func(x_curve, *popt)
        plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num} Curve')

        # 打印拟合曲线方程式并保存到文件
        equation_str = f'Cluster {cluster_num} Equation: '
        for i in range(num_curves):
            a, b, c, d = popt[i * 4:i * 4 + 4]
            equation_str += f'{a:.2f}x^3 + {b:.2f}x^2 + {c:.2f}x + {d:.2f}   '
        print(equation_str)

        # 保存方程式到文件
        with open(f'cluster_function_{cluster_num}.txt', 'w') as file:
            file.write(equation_str)

    plt.title('Polynomial Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 4):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_5.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename)

























# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline

import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 定义多条3阶多项式拟合函数
def poly_fit_func(x, *params):
    num_curves = len(params) // 4
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        a, b, c, d = params[i * 4:i * 4 + 4]
        y_fit += a * x**3 + b * x**2 + c * x + d
    return y_fit

# 定义执行谱聚类和拟合的函数
def cluster_and_fit(filename, iteration):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 1  # 设置要分类的簇数，根据数据情况进行调整
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')
    cluster_labels = model.fit_predict(data)

    # 提取簇的数据并进行多条3阶多项式拟合
    fitted_curves = {}  # 用于保存每个簇的拟合曲线方程式和数据
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用多条3阶多项式拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(poly_fit_func, x_fit, y_fit, p0=initial_params)

            # 保存拟合曲线方程式和数据到字典
            fitted_curves[cluster_num] = {
                'equation': popt,
                'data': cluster_data
            }

    # 绘制聚类结果和所有拟合曲线
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow', label='Original Data')
    for cluster_num, curve_data in fitted_curves.items():
        x_fit = curve_data['data'][:, 0]
        y_fit = curve_data['data'][:, 1]
        popt = curve_data['equation']

        # 绘制拟合曲线
        x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
        y_curve = poly_fit_func(x_curve, *popt)
        plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num} Curve')

        # 打印拟合曲线方程式并保存到文件
        equation_str = f'Cluster {cluster_num} Equation: '
        for i in range(num_curves):
            a, b, c, d = popt[i * 4:i * 4 + 4]
            equation_str += f'{a:.10f}x^3 + {b:.10f}x^2 + {c:.10f}x + {d:.10f}   '
        print(equation_str)

        # 保存方程式到文件
        with open(f'cluster_function_{iteration}_cluster_{cluster_num}.txt', 'w') as file:
            file.write(equation_str + '\n')

    plt.title('Polynomial Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 36):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_5.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename, iteration=i)



def read_equation(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("Cluster 0 Equation"):
                equation = line.split(":")[1].strip()
                return equation
    return None

def main():
    max_n = 36  # Set the maximum value of n for iteration

    for n in range(1, max_n + 1):
        cluster_function_file = f"/content/cluster_function_{n}_cluster_0.txt"
        output_file = f"/content/claculate_{n}.txt"

        # Read equation from cluster_function_n_cluster_0.txt
        equation_str = read_equation(cluster_function_file)

        if equation_str:
            # Write equation to calculate_n.txt
            with open(output_file, 'w') as outfile:
                outfile.write(f"y = {equation_str}")

            print(f"Equation successfully written to {output_file}.")
        else:
            print(f"Error: Cluster 0 Equation not found in {cluster_function_file}.")

if __name__ == "__main__":
    main()

def read_formula_from_file(file_path):
    with open(file_path, 'r') as file:
        formula = file.readline().strip()

    if formula.startswith('y ='):
        formula = formula[3:].strip()  # Remove 'y =' from the formula

        # If the formula does not end with 'x', add it for a complete formula
        if not formula.endswith('x'):
            formula += 'x'

        return formula
    else:
        return None

def find_min_max_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()

    # Extract the first column values as integers
    first_column_values = [int(line.split()[0]) for line in data]

    # Find the minimum and maximum values
    min_value = min(first_column_values)
    max_value = max(first_column_values)

    return min_value, max_value

if __name__ == "__main__":
    num_files = 36  # Change this number to the desired range of files

    for n in range(1, num_files + 1):
        formula_file_path = f"/content/claculate_{n}.txt"
        cluster_file_path = f"/content/cluster_{n}.txt"

        formula = read_formula_from_file(formula_file_path)
        if formula:
            print(f"Formula {n}:", formula)
        else:
            print(f"No valid formula found in the file {formula_file_path}.")

        min_val, max_val = find_min_max_from_file(cluster_file_path)
        print(f"Minimum value for file {n}:", min_val)
        print(f"Maximum value for file {n}:", max_val)

import math
import os

def read_coefficients(filename):
    with open(filename, 'r') as file:
        equation = file.read().strip()
        parts = equation.split(' ')
        a, b, c, d = map(float, [parts[2].split('x^3')[0], parts[4].split('x^2')[0], parts[6].split('x')[0], parts[8]])
        return a, b, c, d

def calculate_y(x, coefficients):
    coefficient_3, coefficient_2, coefficient_1, coefficient_0 = coefficients
    y = coefficient_3 * math.pow(x, 3) + coefficient_2 * math.pow(x, 2) + coefficient_1 * x + coefficient_0
    return y

def find_min_max_from_file(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()

    # Extract the first column values as integers
    first_column_values = [int(line.split()[0]) for line in data]

    # Find the minimum and maximum values
    min_value = min(first_column_values)
    max_value = max(first_column_values)

    return min_value, max_value

if __name__ == "__main__":
    try:
        # Get the list of files with names "/content/claculate_n.txt" where n is a number
        file_list = [filename for filename in os.listdir("/content") if filename.startswith("claculate_") and filename.endswith(".txt")]

        for filename in file_list:
            # Read coefficients from the file
            coefficients = read_coefficients(os.path.join("/content", filename))

            # Find the minimum and maximum value from the corresponding "cluster_n.txt" file
            cluster_file_path = "/content/cluster_" + filename[10:-4] + ".txt"
            min_val, max_val = find_min_max_from_file(cluster_file_path)

            # Calculate and save the X and Y values as coordinate points in "finished_fibres_n.txt"
            coordinates = []
            with open(os.path.join("/content", "finished_fibres_" + filename[10:]), "w") as outfile:
                for x_value in range(int(min_val), int(max_val) + 1):
                    result = calculate_y(x_value, coefficients)
                    rounded_result = round(result)
                    coordinates.append((x_value, rounded_result))
                    outfile.write(f"({x_value}, {rounded_result})\n")

            print(f"计算结果已保存到 'finished_fibres_{filename[10:]}' 文件中。")

    except FileNotFoundError:
        print("文件未找到。")

import os

def read_coordinates_from_file(file_path):
    coordinates = set()
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(int, line.strip()[1:-1].split(','))
            coordinates.add((x, y))
    return coordinates

def write_coordinates_to_file(coordinates, output_file):
    with open(output_file, 'w') as file:
        for coord in coordinates:
            file.write(f'({coord[0]}, {coord[1]})\n')

def main():
    input_folder = "/content/"
    output_file = "/content/merged_coordinates.txt"

    all_coordinates = set()

    for filename in os.listdir(input_folder):
        if filename.startswith("finished_fibres_") and filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            coordinates = read_coordinates_from_file(file_path)
            all_coordinates.update(coordinates)

    write_coordinates_to_file(all_coordinates, output_file)
    print("All coordinates have been merged and duplicates removed.")

if __name__ == "__main__":
    main()

def read_coordinates_from_file(file_path):
    coordinates = set()
    with open(file_path, 'r') as file:
        for line in file:
            # Assuming the coordinates are in the format (x, y)
            # You may need to adjust this part if the format is different
            x, y = map(int, line.strip()[1:-1].split(','))
            coordinates.add((x, y))
    return coordinates

def write_coordinates_to_file(coordinates, output_file_path):
    with open(output_file_path, 'w') as file:
        for coord in coordinates:
            file.write(f"({coord[0]}, {coord[1]})\n")

def main(n):
    all_coordinates = set()
    for i in range(1, n + 1):
        file_path = f"/content/finished_fibres_{i}.txt"
        coordinates = read_coordinates_from_file(file_path)
        all_coordinates.update(coordinates)

    output_file_path = "/content/combined_coordinates.txt"
    write_coordinates_to_file(all_coordinates, output_file_path)
    print("All coordinates have been combined and duplicates removed.")

if __name__ == "__main__":
    n = int(input("Enter the value of n: "))
    main(n)

from PIL import Image

def read_coordinates_from_file(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            x, y = map(int, line.strip()[1:-1].split(','))
            coordinates.append((x, y))
    return coordinates

def create_image_with_coordinates(coordinates):
    img = Image.new("L", (256, 256), color=255)  # Create a white 256x256 image (grayscale)
    pixels = img.load()

    for coord in coordinates:
        x, y = coord
        if 0 <= x < 256 and 0 <= y < 256:
            pixels[x, y] = 0  # Set the pixel at (x, y) to black (pixel value 0)

    return img

def main():
    input_file_path = "/content/combined_coordinates.txt"
    coordinates = read_coordinates_from_file(input_file_path)
    img = create_image_with_coordinates(coordinates)

    output_file_path = "/content/result_image.png"
    img.save(output_file_path)

if __name__ == "__main__":
    main()













import numpy as np
from sklearn.cluster import SpectralClustering
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Sigmoid function for S-shaped curve fitting
def sigmoid(x, L, k, x0):
    return L / (1 + np.exp(-k*(x - x0)))

# Define the function for S-shaped curve fitting
def s_curve_fit_func(x, *params):
    num_curves = len(params) // 3
    y_fit = np.zeros_like(x)
    for i in range(num_curves):
        L, k, x0 = params[i * 3:i * 3 + 3]
        y_fit += sigmoid(x, L, k, x0)
    return y_fit

# Define the main function cluster_and_fit for S-shaped curve fitting
def cluster_and_fit(filename, iteration):
    data = np.loadtxt(filename)

    # 提取X和Y坐标
    X = data[:, 0].reshape(-1, 1)
    Y = data[:, 1].reshape(-1, 1)

    # 使用谱聚类算法将坐标点分类
    n_clusters = 2  # 设置要分类的簇数，根据数据情况进行调整
    n_neighbors = min(2, len(data) - 1)  # 设置最近邻居的数量，并确保不超过样本数量
    model = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', n_neighbors=n_neighbors)
    cluster_labels = model.fit_predict(data)

    # 提取簇的数据并进行S-shaped曲线拟合
    fitted_curves = {}  # 用于保存每个簇的拟合曲线方程式和数据
    for cluster_num in range(n_clusters):
        cluster_data = data[cluster_labels == cluster_num]
        if len(cluster_data) > 0:
            x_fit = cluster_data[:, 0]
            y_fit = cluster_data[:, 1]

            # 使用S-shaped曲线拟合函数进行拟合
            num_curves = 1  # 设置每个簇拟合的曲线数，根据数据情况进行调整
            initial_params = [1.0, 1.0, 1.0] * num_curves
            popt, _ = curve_fit(s_curve_fit_func, x_fit, y_fit, p0=initial_params)

            # 保存拟合曲线方程式和数据到字典
            fitted_curves[cluster_num] = {
                'equation': popt,
                'data': cluster_data
            }

    # 绘制聚类结果和所有拟合曲线
    plt.scatter(X, Y, c=cluster_labels, cmap='rainbow', label='Original Data')
    for cluster_num, curve_data in fitted_curves.items():
        x_fit = curve_data['data'][:, 0]
        y_fit = curve_data['data'][:, 1]
        popt = curve_data['equation']

        # 绘制拟合曲线
        x_curve = np.linspace(min(x_fit), max(x_fit), 1000)
        y_curve = s_curve_fit_func(x_curve, *popt)
        plt.plot(x_curve, y_curve, label=f'Cluster {cluster_num} Curve')

        # 打印拟合曲线方程式并保存到文件
        equation_str = f'Cluster {cluster_num} Equation: '
        for i in range(num_curves):
            L, k, x0 = popt[i * 3:i * 3 + 3]
            equation_str += f'{L:.10f} / (1 + exp(-{k:.10f}*(x - {x0:.10f})))   '
        print(equation_str)

        # 保存方程式到文件
        with open(f'cluster_function_{iteration}_cluster_{cluster_num}.txt', 'w') as file:
            file.write(equation_str + '\n')

    plt.title('S-Shaped Curve Fitting')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

# 多次执行程序
for i in range(1, 44):  # 假设数据文件名为cluster_1.txt, cluster_2.txt, ..., cluster_43.txt
    filename = f'/content/cluster_{i}.txt'
    cluster_and_fit(filename, iteration=i)

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_pixel_frequency(image_path):
    # 打开图像并转换为灰度模式
    img = Image.open(image_path).convert("L")

    # 将图像数据转换为NumPy数组
    img_array = np.array(img)

    # 计算像素值的频率
    pixel_values, pixel_counts = np.unique(img_array, return_counts=True)

    # 绘制频率图
    plt.bar(pixel_values, pixel_counts, color='gray')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Pixel Value Frequency Distribution')
    plt.show()

if __name__ == "__main__":
    image_path = "/content/plot_finished_a_8.png"  # 替换为你的图像文件路径
    plot_pixel_frequency(image_path)

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def plot_pixel_frequency(image_path):
    # 打开图像并转换为灰度模式
    img = Image.open(image_path).convert("L")

    # 将图像数据转换为NumPy数组
    img_array = np.array(img)

    # 删除像素值为0和255的点
    img_array = img_array[(img_array > 0) & (img_array < 255)]

    # 计算像素值的频率
    pixel_values, pixel_counts = np.unique(img_array, return_counts=True)

    # 绘制频率图
    plt.bar(pixel_values, pixel_counts, color='gray')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Pixel Value Frequency Distribution')
    plt.show()

if __name__ == "__main__":
    image_path = "/content/plot_finished_a_8.png"  # 替换为你的图像文件路径
    plot_pixel_frequency(image_path)

import numpy as np
from PIL import Image

def process_images(image1_path, image2_path):
    # 打开两张图像并转换为灰度模式
    img1 = Image.open(image1_path).convert("L")
    img2 = Image.open(image2_path).convert("L")

    # 将图像数据转换为NumPy数组
    img1_array = np.array(img1)
    img2_array = np.array(img2)

    # 计算像素值差异
    pixel_diff = img1_array - img2_array

    # 根据差异设置新的像素值
    processed_array = np.where(pixel_diff > 0, 255, 0)

    # 创建新的图像对象
    processed_image = Image.fromarray(processed_array.astype(np.uint8))

    return processed_image

if __name__ == "__main__":
    image1_path = "/content/plot_finished_a_9.png"  # 替换为第一张图像文件路径
    image2_path = "/content/plot_finished_a_8.png"  # 替换为第二张图像文件路径

    new_image = process_images(image1_path, image2_path)
    new_image.save("output_image.jpg")  # 保存生成的新图像