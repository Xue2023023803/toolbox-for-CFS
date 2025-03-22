import numpy as np
import matplotlib.pyplot as plt
import random

# 参数设置
N = 20  # 点的总数
if N % 2 != 0:
    print(f"点阵必须是偶数，当前{N}不是偶数。")
    N = None
m = 500  # 总面积 (平方厘米)
size = (271, 271)  # 图像的尺寸 (像素)，可以更改为其他值
num_images = 10  # 需要生成的图像数量，可以调整
line_length_factor = 2  # 连接线长度是圆点半径的倍数
line_width = 0.1  # 0-10 之间的值较为常见,0即没有线
line_color = 'white'
# 连接线的颜色，颜色的选择可以通过多种方式指定，常见的方式包括：标准颜色名称：例如 'red', 'blue', 'green', 'black', 'yellow', 'cyan', 'magenta', 'white' 等等。/
# 十六进制颜色代码：例如 '#FF0000'（红色），'#00FF00'（绿色），'#0000FF'（蓝色）。/
# RGB 或 RGBA 色值：例如 (1, 0, 0) 表示红色，(0, 1, 0) 表示绿色，(0, 0, 1) 表示蓝色；RGBA 还可以包含透明度（例如 (0, 1, 0, 0.5) 表示绿色并带有 50% 透明度）。/
# 灰度值：例如 0 表示黑色，1 表示白色，介于之间的值表示灰色。



def generate_dot_matrix(N, m, line_length_factor):
    # 每个点的面积是总面积除以点的数量
    area_per_dot = m / N  # 每个点的面积
    radius_per_dot = np.sqrt(area_per_dot / np.pi)  # 每个点的半径
    diameter_per_dot = 2 * radius_per_dot  # 每个点的直径

    # 增大区域的边长，避免点之间过于拥挤
    side_length = np.sqrt(m) * 2  # 增大边长，确保有足够空间

    points = []
    max_attempts = 1000  # 最大尝试次数，防止死循环
    forbidden_area = []  # 禁止生成点的区域（存储每对点周围的矩形区域）

    # 每次生成两个点，距离固定为半径 * 3
    for _ in range(N // 2):  # 一次生成两个点，N//2次
        attempts = 0
        while attempts < max_attempts:
            # 随机选择第一个点的坐标
            x1 = np.random.uniform(0, side_length)
            y1 = np.random.uniform(0, side_length)

            # 随机生成第二个点，距离固定为 radius * 3
            angle = np.random.uniform(0, 2 * np.pi)  # 随机生成角度
            x2 = x1 + line_length_factor * radius_per_dot * np.cos(angle)
            y2 = y1 + line_length_factor * radius_per_dot * np.sin(angle)

            # 确保第二个点在区域内
            if 0 <= x2 <= side_length and 0 <= y2 <= side_length:
                # 检查这对点是否与已存在的点重叠
                overlap = False
                for (xi, yi) in points:
                    if np.sqrt((x1 - xi) ** 2 + (y1 - yi) ** 2) < diameter_per_dot or \
                            np.sqrt((x2 - xi) ** 2 + (y2 - yi) ** 2) < diameter_per_dot:
                        overlap = True
                        break

                if not overlap:
                    # 将这对点加入到点列表
                    points.append((x1, y1))
                    points.append((x2, y2))

                    # 标记这对点的周围区域为禁区（为了避免交叉）
                    forbidden_area.append(((x1, y1), (x2, y2)))
                    break

            attempts += 1

        # 如果尝试次数超过最大限制，输出警告
        if attempts == max_attempts:
            print("警告: 超过最大尝试次数，点的位置可能存在重叠!")

    return np.array(points), radius_per_dot, forbidden_area


def plot_dot_matrix(xy_points, radius, size, image_index, line_length_factor, forbidden_area, scale_factor=1, line_width=0.7, line_color='cyan'):
    # 创建一个指定大小的图形，单位为英寸
    dpi = 100  # 每英寸的像素数
    figsize = (size[0] / dpi, size[1] / dpi)  # 根据像素大小调整图像尺寸

    plt.figure(figsize=figsize, dpi=dpi)

    # 设置整个图形区域的背景为灰色
    plt.gcf().set_facecolor('gray')  # 图形背景
    plt.gca().set_facecolor('gray')  # 坐标区域背景

    # 绘制每个点，设置圆点为白色
    x, y = xy_points[:, 0], xy_points[:, 1]
    plt.scatter(x, y, s=np.pi * (radius ** 2) * scale_factor, c='white', edgecolors='w', alpha=0.7)

    # 绘制连接线
    for (x1, y1), (x2, y2) in forbidden_area:
        plt.plot([x1, x2], [y1, y2], color=line_color, lw=line_width)  # 使用传入的参数控制线条的颜色和粗细

    plt.gca().set_aspect('equal', adjustable='box')

    # 去除标题和坐标轴
    plt.gca().set_xticks([])
    plt.gca().set_yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # 生成文件名：N #点的总数 + 是第几张生成的图片
    filename = f"connected_{N}_image{image_index}.png"

    # 保存图像到文件
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)




# 循环生成多个图像
for i in range(1, num_images + 1):
    # 生成点阵
    points, radius, forbidden_area = generate_dot_matrix(N, m, line_length_factor)

    # 绘制点阵并保存为图像
    plot_dot_matrix(points, radius, size=size, image_index=i, line_length_factor=line_length_factor,
                    forbidden_area=forbidden_area, scale_factor=1, line_width=line_width, line_color=line_color)
