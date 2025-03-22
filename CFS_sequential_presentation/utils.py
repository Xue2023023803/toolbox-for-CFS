# utils_2.py
from psychopy import visual,core,event
import random
import os
import csv
import numpy as np
import math
from collections import deque

def validate_field_size_and_dot_size(field_size, dot_size, num_dots):
    """
    验证生成区域和点大小是否合理。
    - field_size: 点阵生成区域大小 (width, height)
    - dot_size: 每个点的大小
    - num_dots: 需要生成的点数量
    """
    # 扣除点大小后的实际可用区域
    usable_width = field_size[0] - dot_size
    usable_height = field_size[1] - dot_size
    # 计算最大可放置点的数量
    max_dots_possible = (usable_width // dot_size) * (usable_height // dot_size)

    if num_dots > max_dots_possible:
        raise ValueError(
            f"区域大小 {field_size} 对于 {num_dots} 个点和每个点大小为 {dot_size} 的情况太小了。"
            f" 最大可放置的点数是: {max_dots_possible}."
        )





##########################################################################################################################



def generate_non_overlapping_positions(
        center,
        field_size,
        num_dots,
        radius,
        max_attempts=500000,
        radius_factor=1.5,
        sparsity_factor=0.8  # 新增稀疏性控制参数（建议1.0~1.5）
):
    """
    使用改进泊松盘采样生成非重叠点的位置
    - 强制初始点位于区域中心
    - 通过sparsity_factor控制稀疏程度
    """
    # 初始化参数
    positions = []
    half_width, half_height = field_size[0] / 2, field_size[1] / 2

    # 有效生成区域边界（考虑点半径）
    min_x = center[0] - half_width + radius
    max_x = center[0] + half_width - radius
    min_y = center[1] - half_height + radius
    max_y = center[1] + half_height - radius

    # 场区域原点坐标（用于网格计算）
    field_min_x = center[0] - half_width
    field_min_y = center[1] - half_height

    # 计算最小间距（核心修改点）
    base_min_dist = 2 * radius * sparsity_factor  # 基础最小间距
    area = field_size[0] * field_size[1]
    ideal_spacing = math.sqrt(area / num_dots) * sparsity_factor  # 理想间距
    min_dist = max(base_min_dist, ideal_spacing)  # 最终使用较大值

    # 网格参数（基于实际最小距离）
    grid_size = min_dist / math.sqrt(2)
    grid_width = int(math.ceil(field_size[0] / grid_size))
    grid_height = int(math.ceil(field_size[1] / grid_size))
    grid = [[None] * grid_height for _ in range(grid_width)]

    # ----------- 网格辅助函数 -----------
    def grid_key(x, y):
        """将绝对坐标转换为网格坐标"""
        rel_x = x - field_min_x
        rel_y = y - field_min_y
        gx = int(rel_x // grid_size)
        gy = int(rel_y // grid_size)
        return (
            max(0, min(gx, grid_width - 1)),
            max(0, min(gy, grid_height - 1))
        )

    def is_valid(x, y):
        """检查点是否满足最小间距要求"""
        gx, gy = grid_key(x, y)
        # 检查周围3x3网格
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                ngx = gx + dx
                ngy = gy + dy
                if 0 <= ngx < grid_width and 0 <= ngy < grid_height:
                    p = grid[ngx][ngy]
                    if p is not None:
                        dist_sq = (x - p[0]) ** 2 + (y - p[1]) ** 2
                        if dist_sq < min_dist ** 2:
                            return False
        return True

    def add_point(x, y):
        """将有效点加入系统"""
        if not (min_x <= x <= max_x and min_y <= y <= max_y):
            return False
        gx, gy = grid_key(x, y)
        if grid[gx][gy] is None:
            grid[gx][gy] = (x, y)
            positions.append((x, y))
            return True
        return False

    # ----------- 生成逻辑 -----------
    attempts = 0
    activity_list = deque()

    # 强制初始点在中心（关键修改）
    center_x, center_y = center
    if add_point(center_x, center_y):
        activity_list.append((center_x, center_y))
    else:
        # 如果中心被阻挡则尝试附近随机点
        found = False
        for _ in range(100):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(0, 2 * radius)
            x = center_x + dist * math.cos(angle)
            y = center_y + dist * math.sin(angle)
            if add_point(x, y):
                activity_list.append((x, y))
                found = True
                break
        if not found:
            return []  # 完全无法放置初始点

    # 阶段1：活动队列引导生成
    k_candidates = 20  # 每次生成候选点数
    while activity_list and len(positions) < num_dots and attempts < max_attempts:
        current = activity_list.popleft()
        for _ in range(k_candidates):
            attempts += 1
            angle = random.uniform(0, 2 * math.pi)
            # 在[min_dist, radius_factor*min_dist]范围内生成
            distance = random.uniform(min_dist, radius_factor * min_dist)
            x = current[0] + distance * math.cos(angle)
            y = current[1] + distance * math.sin(angle)

            if add_point(x, y):
                activity_list.append((x, y))
                break  # 成功生成则停止当前点的候选

    # 阶段2：全局随机填充剩余点
    while len(positions) < num_dots and attempts < max_attempts:
        attempts += 1
        # 优先尝试从现有点扩展
        if positions:
            base = random.choice(positions)
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(min_dist, radius_factor * min_dist)
            x = base[0] + distance * math.cos(angle)
            y = base[1] + distance * math.sin(angle)
        else:  # 极端情况直接随机
            x = random.uniform(min_x, max_x)
            y = random.uniform(min_y, max_y)

        if add_point(x, y):
            activity_list.append((x, y))

    print(f"生成结果: {len(positions)}/{num_dots} 点 (尝试次数: {attempts})")
    return positions
















def generate_connected_positions(big_circle_positions, radius, num_pairs, max_attempts=5000):
    """
    根据大圆位置生成连接点的小圆圆心位置。
    - big_circle_positions: 大圆的位置列表，每个元素是一个 (x, y) 坐标
    - radius: 中圆的半径，连接点的位置位于这个半径上
    - num_pairs: 连接点对的数量（每对由两个点组成）
    - max_attempts: 尝试生成连接点的最大次数
    返回:
    - positions: 连接点的位置列表，每个元素是一个 (x1, y1) 和 (x2, y2)
    """
    x_positions = []  # 存储所有点的 x 坐标
    y_positions = []  # 存储所有点的 y 坐标
    attempts = 0

    # 复制一份大圆位置列表用于不放回的抽取
    available_positions = big_circle_positions[:]

    while len(x_positions) < 2 * num_pairs and attempts < max_attempts:  # num_pairs 对应 num_pairs * 2 点
        if not available_positions:
            break  # 如果没有更多大圆位置了，跳出

        # 从剩余大圆位置中随机选择一个位置（不放回）
        big_circle_center = random.choice(available_positions)
        available_positions.remove(big_circle_center)  # 删除已选位置，防止重复

        # 生成一对对称位置
        angle1 = random.uniform(0, 2 * np.pi)  # 第一个连接点的角度
        angle2 = angle1 + np.pi  # 第二个连接点与第一个对称

        # 计算第一个点的位置
        x1 = big_circle_center[0] + (radius * 2) * np.cos(angle1)  # 使用 radius * 2 来生成距离为 4 * radius
        y1 = big_circle_center[1] + (radius * 2) * np.sin(angle1)

        # 计算第二个点的位置
        x2 = big_circle_center[0] + (radius * 2) * np.cos(angle2)
        y2 = big_circle_center[1] + (radius * 2) * np.sin(angle2)

        # 将两个点的坐标分别加入 x_positions 和 y_positions
        x_positions.append(x1)
        y_positions.append(y1)
        x_positions.append(x2)
        y_positions.append(y2)

        attempts += 1

    # 将 x 和 y 坐标组合成 (x, y) 的二维数组
    final_positions = np.column_stack((x_positions, y_positions))

    return final_positions




#########################################################################################################################
def generate_noise_positions_from_target(positions_target, noise_shift):
    """
    根据 target 区域的点阵位置生成对应的噪声位置。
    假设噪声区域通过对 target 区域进行平移来生成。
    还使用 `field_size` 和 `dot_size` 来确保生成的点不会超出噪声区域的边界。
    """
    noise_positions = []

    for x, y in positions_target:
        # 将 target 区域的点平移到噪声区域的位置
        noise_x = x + noise_shift[0]
        noise_y = y + noise_shift[1]

        noise_positions.append((noise_x, noise_y))

    return noise_positions


def collect_subject_info(win, target_position, noise_position):
    """
    弹出四个输入框让被试输入姓名和编号，并将信息保存到CSV文件中。
    两个框用于姓名输入，一个在目标位置，一个在噪声位置；
    另外两个框用于被试编号输入，也分别在目标位置和噪声位置。
    """
    # 文件名
    file_name = "Experimental_data_results/B_cfs_experiment_subject_Mapping.csv"
    font = "Times New Roman"  # 字体设定

    # 检查文件是否存在，如果不存在，创建新文件
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["subject_name", "subject_id", "dominant_eye"])  # 已添加新字段

    # 创建优势眼提示文本（下移版本）
    dominant_eye_text_target = visual.TextStim(win, text="优势眼: ", height=30,
                                               pos=(target_position[0], target_position[1] - 160),  # 原-100 → -160
                                               color='black')
    dominant_eye_text_noise = visual.TextStim(win, text="优势眼: ", height=30,
                                              pos=(noise_position[0], noise_position[1] - 160),  # 原-100 → -160
                                              color='black')
    eye_prompt = visual.TextStim(win, text="←/→ 选择，Tab确认", height=20,
                                 pos=(target_position[0], target_position[1] - 200),  # 原-140 → -200
                                 color='white')

    # 创建提示文本
    prompt_text_target = visual.TextStim(win, text="按Enter键提交\n按Tab键切换输入框", height=20,
                                         pos=(target_position[0], target_position[1] + 60),  # 原-120 → +60
                                         color='white')
    prompt_text_noise = visual.TextStim(win, text="按Enter键提交\n按Tab键切换输入框", height=20,
                                        pos=(noise_position[0], noise_position[1] + 60),  # 原-120 → +60
                                        color='white')

    # 创建显示文本框的位置，左侧的框错开垂直位置
    subject_name_text_target = visual.TextStim(win, text="姓名: ", height=30,
                                               pos=(target_position[0], target_position[1] + 20), color='black')
    subject_name_text_noise = visual.TextStim(win, text="姓名: ", height=30,
                                              pos=(noise_position[0], noise_position[1] + 20), color='black')

    subject_id_text_target = visual.TextStim(win, text="被试编号: ", height=30,
                                             pos=(target_position[0], target_position[1] - 40), color='black')
    subject_id_text_noise = visual.TextStim(win, text="被试编号: ", height=30,
                                            pos=(noise_position[0], noise_position[1] - 40), color='black')

    # 显示提示文本
    prompt_text_target.draw()
    prompt_text_noise.draw()
    subject_name_text_target.draw()
    subject_name_text_noise.draw()
    subject_id_text_target.draw()
    subject_id_text_noise.draw()

    # 新增部分：绘制优势眼相关元素
    eye_prompt.draw()
    dominant_eye_text_target.draw()
    dominant_eye_text_noise.draw()

    win.flip()

    subject_name = ""
    subject_id = ""
    dominant_eye = ""  # 新增变量

    # 当前焦点框的索引，控制Tab切换
    focus_index = 0  # 0: 姓名框（目标位置），1: 编号框（目标位置），2: 优势眼

    while True:
        keys = event.getKeys()

        # 处理输入框的输入
        if 'escape' in keys:  # 如果按下Escape退出
            return None, None  # 返回None表示取消输入

        # Tab键切换焦点（现在有三个切换项）
        if 'tab' in keys:
            focus_index = (focus_index + 1) % 3  # 修改为3个切换项

        # 新增部分：处理优势眼选择
        if focus_index == 2:
            if 'left' in keys:
                dominant_eye = "左眼"
            elif 'right' in keys:
                dominant_eye = "右眼"

        # 如果按下退格键，则删除最后一个字符
        if 'backspace' in keys:
            if focus_index == 0:  # 姓名框
                subject_name = subject_name[:-1]
            elif focus_index == 1:  # 编号框
                subject_id = subject_id[:-1]

        # 如果按下Enter键，则获取输入内容
        if 'return' in keys:
            # 新增：检查优势眼是否选择
            if not dominant_eye:
                warning_text = visual.TextStim(win, text="请选择优势眼！", color='red', height=30)
                warning_text.setPos(target_position)
                warning_text.draw()
                warning_text.setPos(noise_position)
                warning_text.draw()
                win.flip()
                core.wait(1.5)
                continue

            # 检查输入的被试编号是否已存在
            with open(file_name, mode='r', newline='') as f:
                reader = csv.reader(f)
                next(reader)  # 跳过表头
                existing_ids = [row[1] for row in reader]  # 获取已有的被试编号

            if subject_id in existing_ids:
                # 如果已存在该被试编号，弹窗警告
                warning_text = visual.TextStim(win, text=f"警告: 被试编号 {subject_id} 已存在！\n请检查输入。",
                                               pos=(0, 0), color='red', height=30)

                # 同时在目标和噪声位置显示警告
                warning_text.setPos(target_position)
                warning_text.draw()
                warning_text.setPos(noise_position)
                warning_text.draw()

                win.flip()
                core.wait(2)  # 显示警告2秒

                # 清空输入框，继续等待重新输入
                subject_name = ""
                subject_id = ""
                dominant_eye = ""  # 新增：重置优势眼
                subject_name_text_target.setText("姓名: ")
                subject_name_text_noise.setText("姓名: ")
                subject_id_text_target.setText("被试编号: ")
                subject_id_text_noise.setText("被试编号: ")
                prompt_text_target.draw()
                prompt_text_noise.draw()
                subject_name_text_target.draw()
                subject_name_text_noise.draw()
                subject_id_text_target.draw()
                subject_id_text_noise.draw()
                win.flip()
                continue  # 继续等待输入
            else:
                # 如果被试编号不存在，则保存信息到CSV
                with open(file_name, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([subject_name, subject_id, dominant_eye])  # 新增字段

                # 返回被试的姓名和编号
                return subject_name, subject_id,dominant_eye

        # 更新输入框的文本
        subject_name_text_target.setText(f"姓名: {subject_name}")
        subject_name_text_noise.setText(f"姓名: {subject_name}")
        subject_id_text_target.setText(f"被试编号: {subject_id}")
        subject_id_text_noise.setText(f"被试编号: {subject_id}")
        dominant_eye_text_target.setText(f"优势眼: {dominant_eye}")  # 新增更新显示
        dominant_eye_text_noise.setText(f"优势眼: {dominant_eye}")  # 新增更新显示

        # 绘制并更新窗口
        subject_name_text_target.draw()
        subject_name_text_noise.draw()
        subject_id_text_target.draw()
        subject_id_text_noise.draw()
        prompt_text_target.draw()
        prompt_text_noise.draw()
        dominant_eye_text_target.draw()  # 新增绘制
        dominant_eye_text_noise.draw()  # 新增绘制
        eye_prompt.draw()  # 新增绘制
        win.flip()

        # 等待一定时间，避免CPU占用过高
        core.wait(0.05)

        # 处理键盘输入：按下字母或数字则加入文本
        for key in keys:
            if len(key) == 1 and key.isalnum():  # 如果是字母或数字
                if focus_index == 0:  # 姓名框
                    subject_name += key
                elif focus_index == 1:  # 编号框
                    subject_id += key




def fusion_point(win,target_position,noise_position,image_folder_path):
    # 初始化实验参数


    # 获取文件夹内所有图像文件的路径
    image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if
                   f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if len(image_files) == 1:
        image_file = image_files[0]  # 获取单个图像文件的路径
    else:
        print("文件夹中存在多个图片,需要删除多余图片")
        return  # 如果文件夹中有多于一个图片，函数提前返回

    # 加载图像并创建ImageStim对象
    image_stim_left = visual.ImageStim(win, image=image_file, pos=target_position)
    image_stim_right = visual.ImageStim(win, image=image_file, pos=noise_position)

    # 显示图像
    image_stim_left.draw()
    image_stim_right.draw()

    win.flip()

    # 监听空格键
    while True:
        keys = event.waitKeys(keyList=['space'], timeStamped=True)
        if keys:  # 如果有按键被按下
            win.flip()  # 刷新窗口
            break  # 在按下一次空格键后退出循环

    # 获取并打印图像的长宽(调试用)
    # width, height = image_stim_left.size
    # print(f"Image {os.path.basename(image_file)} dimensions: {width} x {height}")











##################################################废弃算法################################################################
def unuse_generate_non_overlapping_positions(center, field_size, num_dots, dot_size, max_attempts=5000, radius_factor=1.5):
    """
    使用泊松盘采样生成非重叠点的位置
    - center: 刺激中心点 (x, y)
    - field_size: 点阵生成区域的宽高 (width, height)
    - num_dots: 点的数量
    - dot_size: 每个点的大小
    - max_attempts: 尝试生成点的最大次数
    - radius_factor: 用于控制候选点生成区域的半径，通常设为 1.5
    返回:
    - positions: 非重叠点的位置列表
    """

    # 初始化变量
    positions = []
    attempts = 0
    half_width, half_height = field_size[0] / 2, field_size[1] / 2
    min_x = center[0] - half_width + dot_size
    max_x = center[0] + half_width - dot_size
    min_y = center[1] - half_height + dot_size
    max_y = center[1] + half_height - dot_size

    # 计算合适的最小距离，考虑点的数量和区域大小
    area = field_size[0] * field_size[1]
    ideal_spacing = math.sqrt(area / num_dots)  # 每个点之间的理想间距
    min_dist = max(dot_size * 2, ideal_spacing)  # 最小距离至少是点直径，最多是理想间距

    # 网格化参数
    grid_size = min_dist / math.sqrt(2)  # 网格单元大小，确保每个点周围都有一定的空间
    grid_width = int(math.ceil(field_size[0] / grid_size))
    grid_height = int(math.ceil(field_size[1] / grid_size))

    # 初始化网格
    grid = [[None] * grid_height for _ in range(grid_width)]

    # 将生成的点保存到网格中
    def grid_key(x, y):
        grid_x = int(x // grid_size)
        grid_y = int(y // grid_size)

        # 调试: 打印网格索引
        if grid_x < 0 or grid_x >= grid_width or grid_y < 0 or grid_y >= grid_height:
            print(f"Invalid grid index: {grid_x}, {grid_y} for point ({x}, {y})")
            # 返回有效范围内的索引
            grid_x = max(0, min(grid_x, grid_width - 1))
            grid_y = max(0, min(grid_y, grid_height - 1))

        return grid_x, grid_y

    # 检查点是否与已放置的点重叠
    def is_valid(x, y):
        grid_x, grid_y = grid_key(x, y)
        # 检查网格中的邻近点
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = grid_x + dx, grid_y + dy
                if 0 <= nx < grid_width and 0 <= ny < grid_height:
                    point = grid[nx][ny]
                    if point is not None:
                        px, py = point
                        if (x - px) ** 2 + (y - py) ** 2 < min_dist ** 2:
                            return False
        return True

    # 将点添加到网格中
    def add_point(x, y):
        grid_x, grid_y = grid_key(x, y)

        # 检查生成的点是否在有效范围内
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            grid[grid_x][grid_y] = (x, y)
            positions.append((x, y))
        else:
            print(f"Skipping invalid point at ({x}, {y}) due to out-of-bounds grid index.")

    # 初始化第一个点
    first_x = random.uniform(min_x, max_x)
    first_y = random.uniform(min_y, max_y)
    add_point(first_x, first_y)

    # 开始泊松盘采样
    while len(positions) < num_dots and attempts < max_attempts:
        attempts += 1
        # 随机选择一个已有点作为“中心”，然后生成候选点
        center_x, center_y = positions[random.randint(0, len(positions) - 1)]
        # 生成候选点，随机选择一个角度和距离
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(min_dist, radius_factor * min_dist)
        candidate_x = center_x + dist * math.cos(angle)
        candidate_y = center_y + dist * math.sin(angle)

        # 检查候选点是否有效
        if min_x <= candidate_x <= max_x and min_y <= candidate_y <= max_y and is_valid(candidate_x, candidate_y):
            add_point(candidate_x, candidate_y)

    if attempts >= max_attempts:
        print("Warning: Unable to generate all non-overlapping positions within the max attempts.")

    return positions






def unuse_generate_connected_positions(big_circle_positions, radius, num_pairs, max_attempts=5000):
    """
    根据大圆位置生成连接点的小圆圆心位置。
    - big_circle_positions: 大圆的位置列表，每个元素是一个 (x, y) 坐标
    - radius: 中圆的半径，连接点的位置位于这个半径上
    - num_pairs: 连接点对的数量（每对由两个点组成）
    - max_attempts: 尝试生成连接点的最大次数
    返回:
    - positions: 连接点的位置列表，每个元素是一个 (x1, y1) 和 (x2, y2)
    """
    x_positions = []  # 存储所有点的 x 坐标
    y_positions = []  # 存储所有点的 y 坐标
    attempts = 0

    # 复制一份大圆位置列表用于不放回的抽取
    available_positions = big_circle_positions[:]

    while len(x_positions) < 2 * num_pairs and attempts < max_attempts:  # num_pairs 对应 num_pairs * 2 点
        if not available_positions:
            break  # 如果没有更多大圆位置了，跳出

        # 从剩余大圆位置中随机选择一个位置（不放回）
        big_circle_center = random.choice(available_positions)
        available_positions.remove(big_circle_center)  # 删除已选位置，防止重复

        # 生成一对对称位置
        angle1 = random.uniform(0, 2 * np.pi)  # 第一个连接点的角度
        angle2 = angle1 + np.pi  # 第二个连接点与第一个对称

        # 计算第一个点的位置
        x1 = big_circle_center[0] + radius * np.cos(angle1)
        y1 = big_circle_center[1] + radius * np.sin(angle1)

        # 计算第二个点的位置
        x2 = big_circle_center[0] + radius * np.cos(angle2)
        y2 = big_circle_center[1] + radius * np.sin(angle2)

        # 将两个点的坐标分别加入 x_positions 和 y_positions
        x_positions.append(x1)
        y_positions.append(y1)
        x_positions.append(x2)
        y_positions.append(y2)

        attempts += 1

    # 将 x 和 y 坐标组合成 (x, y) 的二维数组
    final_positions = np.column_stack((x_positions, y_positions))

    return final_positions