import numpy as np  # 导入 NumPy 库，帮助创建和修改纹理
from psychopy import visual,core
import os
import random


def create_target_stim(win, num_dots, dot_size, field_size, target_position, contrast_level, positions):
    """
    创建目标刺激的点阵并应用对比度控制
    """
    # 创建一个基础的灰度纹理，初始化为 1.0（表示白色，背景亮度为白色时可以进行对比度调节）
    texture_size =field_size[0] # 纹理的尺寸
    base_texture = np.ones((texture_size, texture_size)) * 1.0  # 初始化为白色背景纹理

    # 获取窗口背景颜色，动态计算亮度
    background_color = np.array(win.color)  # 获取背景颜色
    background_luminance = np.mean(background_color)  # 计算背景亮度（假设背景为 RGB 格式）

    # 通过对比度级别调整纹理，使用背景亮度来调整对比度
    adjusted_texture = adjust_contrast(base_texture, contrast_level, background_luminance)

    # 创建 ElementArrayStim，并应用调整后的对比度纹理
    target_stim = visual.ElementArrayStim(
        win,
        nElements=num_dots,
        elementTex=adjusted_texture,  # 使用调整过的对比度纹理
        elementMask="circle",
        sizes=dot_size,
        xys=positions  # 使用已经预计算好的固定位置
    )

    return target_stim



def adjust_contrast(texture, contrast, background_luminance):
    """
    调整纹理的对比度。对比度范围为 [0, 1]。
    contrast 为对比度级别，背景亮度用于对比度计算。
    """


    adjusted_texture = (texture - background_luminance) * contrast + background_luminance  # 根据背景亮度调节对比度
    adjusted_texture = np.clip(adjusted_texture, 0, 1)  # 确保纹理值在 [0, 1] 范围内
    return adjusted_texture



#######################################################################

def generate_stimulus_sequence(win,num_dots, dot_size, field_size, target_position, contrast_levels, stimulus_duration):
    from utils import generate_non_overlapping_positions  # 假设有这个工具函数来生成不重叠的点阵位置

    # 计算并固定位置
    positions = generate_non_overlapping_positions(target_position, field_size, num_dots, dot_size, max_attempts=2000)

    # 存储刺激序列
    stimulus_sequence = []

    levels_total = len(contrast_levels)

    for i in range(levels_total):
        # 获取当前对比度
        contrast_level = contrast_levels[i]

        # 创建目标刺激，并设置对比度
        target_stim = create_target_stim(win, num_dots, dot_size, field_size, target_position, contrast_level, positions)

        # 将刺激对象和相关信息存储在序列中
        stimulus_sequence.append({
            'contrast_level': contrast_level,
            'stimulus': target_stim,
            'duration': stimulus_duration / levels_total
        })



    return stimulus_sequence

####################################################调取法###############################################################
def load_image_stimuli(folder_path):
    """
    加载指定文件夹下每个子文件夹中的图片文件，并按子文件夹名称存储为刺激序列。
    :param folder_path: 主文件夹路径，其中包含若干子文件夹
    :return: 一个字典，键是子文件夹名称，值是该文件夹中的图片刺激序列
    """
    stimuli_dict = {}

    # 遍历目标文件夹下的每个子文件夹
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)

        # 确保是文件夹
        if os.path.isdir(subfolder_path):
            stimuli_list = []

            # 遍历子文件夹中的文件
            for file in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file)

                # 只加载图片文件（假设是png、jpg或jpeg格式）
                if file.lower().endswith(('png', 'jpg', 'jpeg')):
                    stimuli_list.append(file_path)

            # 将图片文件列表存储到字典中，键为子文件夹名
            stimuli_dict[subfolder] = stimuli_list

    return stimuli_dict


def create_stimulus_sequence(win, stimuli_dict):
    """
    根据加载的图片刺激序列，创建一个视觉刺激对象序列。
    :param win: psychopy窗口对象，用于展示图片
    :param stimuli_dict: 图片路径字典，键为子文件夹名，值为图片路径列表
    :return: 一个字典，键是子文件夹名称，值为视觉刺激对象序列
    """
    stim_objects_dict = {}

    for subfolder, image_paths in stimuli_dict.items():
        stim_objects = []

        for img_path in image_paths:
            # 创建视觉刺激对象
            stim = visual.ImageStim(win, image=img_path)
            stim_objects.append(stim)

        stim_objects_dict[subfolder] = stim_objects

    return stim_objects_dict


def create_target_sequence(stim_objects_dict, contrast_levels, num_dots, num_repeats):
    """
    从不同的刺激序列中随机抽取刺激，组成一个新的目标刺激序列，并按照对比度调整。
    :param stim_objects_dict: 传入的刺激对象字典，键是子文件夹名（如：num_dots），值是该文件夹中的图片刺激对象列表
    :param contrast_levels: 需要按照顺序应用的对比度列表
    :param num_dots: 指定从哪个子文件夹（文件夹名为数字）中抽取刺激
    :param num_repeats: 需要从该文件夹抽取多少个刺激
    :return: 生成的目标刺激序列
    """
    target_sequence = []

    if str(num_dots) not in stim_objects_dict:
        print(f"警告：没有找到名称为 {num_dots} 的文件夹，无法进行抽取。")
        return target_sequence

    # 获取指定文件夹（num_dots 对应的文件夹）的刺激序列
    stimulus_list = stim_objects_dict[str(num_dots)]

    if len(stimulus_list) < num_repeats:
        print(f"警告：要求抽取的次数（{num_repeats}）大于文件夹中刺激的数量（{len(stimulus_list)}）。")
        return target_sequence


    # 随机抽取一个刺激
    stim = random.choice(stimulus_list)

    # 根据 contrast_levels 设置每个复制刺激的对比度
    for i in range(num_repeats):
        # 创建一个新的刺激副本（确保对比度设置是独立的）
        stim_copy = visual.ImageStim(stim.win, image=stim.image)

        # 设置复制刺激的对比度
        contrast_level = contrast_levels[i % len(contrast_levels)]  # 按照顺序循环使用对比度
        stim_copy.setContrast(contrast_level)

        # 将该刺激副本添加到目标序列
        target_sequence.append(stim_copy)

    return target_sequence


