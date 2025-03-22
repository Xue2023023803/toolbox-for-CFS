import numpy as np
import matplotlib.pyplot as plt

# 参数设置
N = 2  # 点的总数
m = 500  # 总面积 (平方厘米)
size = (272, 272)  # 图像的尺寸 (像素)，可以更改为其他值
num_images = 10  # 需要生成的图像数量，可以调整

def generate_dot_matrix(N, m):
    # 每个点的面积是总面积除以点的数量
    area_per_dot = m / N  # 每个点的面积
    radius_per_dot = np.sqrt(area_per_dot / np.pi)  # 每个点的半径
    diameter_per_dot = 2 * radius_per_dot  # 每个点的直径

    # 增大区域的边长，避免点之间过于拥挤
    side_length = np.sqrt(m) * 2  # 增大边长，确保有足够空间

    # 初始化点的位置
    x, y = [], []
    max_attempts = 1000  # 最大尝试次数，防止死循环
    for _ in range(N):
        attempts = 0
        while attempts < max_attempts:
            new_x = np.random.uniform(0, side_length)
            new_y = np.random.uniform(0, side_length)

            # 检查新点是否与已有的点重叠
            if all(np.sqrt((new_x - xi) ** 2 + (new_y - yi) ** 2) >= diameter_per_dot for xi, yi in zip(x, y)):
                x.append(new_x)
                y.append(new_y)
                break
            attempts += 1

        # 如果尝试次数超过限制，输出警告
        if attempts == max_attempts:
            print("警告: 超过最大尝试次数，点的位置可能存在重叠!")

    return np.array(x), np.array(y), radius_per_dot

def plot_dot_matrix(x, y, radius, size, image_index, scale_factor=1):
    # 创建一个指定大小的图形，单位为像素
    dpi = 100  # 每英寸的像素数
    figsize = (size[0] / dpi, size[1] / dpi)  # 根据像素大小调整图像尺寸

    # 创建图形
    plt.figure(figsize=figsize, dpi=dpi)

    # 设置整个图形区域的背景为灰色
    plt.gcf().set_facecolor('gray')  # 图形背景
    plt.gca().set_facecolor('gray')  # 坐标区域背景

    # 将点的大小调整为相对于图像的像素大小
    pixel_radius = radius * dpi / size[0]  # 将半径转换为图像像素尺寸

    # 绘制每个点，设置圆点为白色
    plt.scatter(x, y, s=np.pi * (pixel_radius ** 2) * scale_factor, c='white', edgecolors='w', alpha=0.7)
    plt.gca().set_aspect('equal', adjustable='box')

    # 去除标题和坐标轴
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # 生成文件名：N #点的总数 + 是第几张生成的图片
    filename = f"{N}_image{image_index}.png"

    # 保存图像到文件
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    # 关闭图形窗口，避免弹出
    plt.close()

# 循环生成多个图像
for i in range(1, num_images + 1):
    # 生成点阵
    x, y, radius = generate_dot_matrix(N, m)

    # 绘制点阵并保存为图像
    plot_dot_matrix(x, y, radius, size=size, image_index=i, scale_factor=1)
