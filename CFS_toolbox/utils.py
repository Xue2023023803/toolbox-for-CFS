# utils.py
from psychopy import visual,core,event
import random
import os
import csv

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




def generate_non_overlapping_positions(center, field_size, num_dots, dot_size, max_attempts=5000):
    """
    生成非重叠点的位置。
    - center: 刺激中心点 (x, y)
    - field_size: 点阵生成区域的宽高 (width, height)7
    - num_dots: 点的数量
    - dot_size: 每个点的大小
    - max_attempts: 尝试生成点的最大次数
    返回:
    - positions: 非重叠点的位置列表
    """

    positions = []
    attempts = 0
    half_width, half_height = field_size[0] / 2, field_size[1] / 2
    # 生成点时，避免点靠近边缘
    min_x = center[0] - half_width + dot_size
    max_x = center[0] + half_width - dot_size
    min_y = center[1] - half_height + dot_size
    max_y = center[1] + half_height - dot_size


    while len(positions) < num_dots and attempts < max_attempts:
        attempts += 1
        x = random.uniform(min_x, max_x)
        y = random.uniform(min_y, max_y)

        # 检查与现有点是否重叠
        overlap = any((x - px) ** 2 + (y - py) ** 2 < (dot_size * 2) ** 2 for px, py in positions)
        if not overlap:
            positions.append((x, y))

    if attempts >= max_attempts:
        print("Warning: Unable to generate all non-overlapping positions within the max attempts.")
    return positions



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
    file_name = "B_cfs_experiment_subject_Mapping.csv"
    font = "Times New Roman"  # 字体设定

    # 检查文件是否存在，如果不存在，创建新文件
    if not os.path.exists(file_name):
        with open(file_name, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["subject_name", "subject_id"])  # 写入表头

    # 创建提示文本
    prompt_text_target = visual.TextStim(win, text="按Enter键提交\n按Tab键切换输入框", height=20,
                                       pos=(target_position[0], target_position[1] - 120), color='white')
    prompt_text_noise = visual.TextStim(win, text="按Enter键提交\n按Tab键切换输入框", height=20,
                                     pos=(noise_position[0], noise_position[1] - 120), color='white')

    # 创建显示文本框的位置，左侧的框错开垂直位置
    subject_name_text_target = visual.TextStim(win, text="姓名: ", height=30, pos=(target_position[0], target_position[1] + 20), color='black')
    subject_name_text_noise = visual.TextStim(win, text="姓名: ", height=30, pos=(noise_position[0], noise_position[1] + 20), color='black')

    subject_id_text_target = visual.TextStim(win, text="被试编号: ", height=30, pos=(target_position[0], target_position[1] - 40), color='black')
    subject_id_text_noise = visual.TextStim(win, text="被试编号: ", height=30, pos=(noise_position[0], noise_position[1] - 40), color='black')

    # 显示提示文本
    prompt_text_target.draw()
    prompt_text_noise.draw()
    subject_name_text_target.draw()
    subject_name_text_noise.draw()
    subject_id_text_target.draw()
    subject_id_text_noise.draw()
    win.flip()

    subject_name = ""
    subject_id = ""

    # 当前焦点框的索引，控制Tab切换
    focus_index = 0  # 0: 姓名框（目标位置），1: 编号框（目标位置）

    while True:
        keys = event.getKeys()

        # 处理输入框的输入
        if 'escape' in keys:  # 如果按下Escape退出
            return None, None  # 返回None表示取消输入

        # Tab键切换焦点（只在两组框内切换）
        if 'tab' in keys:
            focus_index = (focus_index + 1) % 2  # 姓名框和编号框组内切换

        # 如果按下退格键，则删除最后一个字符
        if 'backspace' in keys:
            if focus_index == 0:  # 姓名框
                subject_name = subject_name[:-1]
            elif focus_index == 1:  # 编号框
                subject_id = subject_id[:-1]

        # 如果按下Enter键，则获取输入内容
        if 'return' in keys:
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
                warning_text.setPos(target_position)  # 设置警告位置为目标位置
                warning_text.draw()

                warning_text.setPos(noise_position)  # 设置警告位置为噪声位置
                warning_text.draw()

                win.flip()
                core.wait(2)  # 显示警告2秒

                # 清空输入框，继续等待重新输入
                subject_name = ""
                subject_id = ""
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
                    writer.writerow([subject_name, subject_id])  # 写入被试信息

                # 返回被试的姓名和编号
                return subject_name, subject_id

        # 更新输入框的文本
        subject_name_text_target.setText(f"姓名: {subject_name}")
        subject_name_text_noise.setText(f"姓名: {subject_name}")
        subject_id_text_target.setText(f"被试编号: {subject_id}")
        subject_id_text_noise.setText(f"被试编号: {subject_id}")

        # 绘制并更新窗口
        subject_name_text_target.draw()
        subject_name_text_noise.draw()
        subject_id_text_target.draw()
        subject_id_text_noise.draw()
        prompt_text_target.draw()
        prompt_text_noise.draw()
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


