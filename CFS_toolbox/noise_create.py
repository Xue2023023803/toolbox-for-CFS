from psychopy import core, event,visual
import numpy as np
from PIL import Image
import os
from psychopy.visual import ImageStim
import random

################################################简单噪声创建##############################################################

def create_noise_sequence(win, noise_stim_size, noise_type, noise_position, noise_frequency, duration):
    """
    生成一个固定更新频率的噪声序列
    - noise_frequency: 每秒更新的噪声帧数（例如 10Hz）
    - duration: 噪声序列持续的总时间
    """
    # 计算噪声序列总共需要多少帧
    num_frames = int(duration * noise_frequency)  # 向上取整生成帧数 （noise_frequence一般是10，所以没关系）

    # 创建一个噪声序列，存储每一帧噪声
    noise_sequence = []
    for _ in range(num_frames):
        noise_stim = visual.NoiseStim(
            win,
            noiseType=noise_type,
            size=(noise_stim_size, noise_stim_size),
            color=[1, 1, 1],
            opacity=1,
            pos=noise_position
        )
        noise_sequence.append(noise_stim)

    return noise_sequence

##################################################加载后处理方法###########################################################

# 读取文件夹中的所有图像
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        if os.path.isfile(img_path) and img_path.lower().endswith(('png', 'jpg', 'jpeg')):
            try:
                img = Image.open(img_path)
                images.append(img)  # 保留PIL图像对象
            except Exception as e:
                print(f"Error opening image {img_path}: {e}")
    return images



# 创建图像刺激序列，并将其扩充到正常的帧数
def create_psychopy_stimulus(win,stimulus_duration,noise_position, noise_stim_size, noise_path ):
    # 读取图像文件夹中的所有图像
    images = load_images_from_folder(noise_path)

    # 创建原始的图像刺激序列
    stimuli = []
    for image in images:
        stimulus = ImageStim(win, image=image, pos=noise_position, size=(noise_stim_size, noise_stim_size), units='pix')
        stimuli.append(stimulus)

    numb_time = stimulus_duration * len(stimuli)
    extend_numb =numb_time - len(stimuli)

    # 扩充刺激序列

    extended_stimuli = random.choices(stimuli, k=extend_numb)

    return extended_stimuli + stimuli





def calculate_rms_contrast(image_array):
    """
    计算图像的 RMS 对比度
    :param image_array: 输入的图像数组
    :return: 图像的 RMS 对比度
    """
    # 计算图像的均值
    mean_value = np.mean(image_array)
    # 计算图像的 RMS 对比度
    rms_contrast = np.sqrt(np.mean((image_array - mean_value) ** 2))

    # 直接使用标准差作为对比度
    rms_contrast = np.std(image_array)

    return rms_contrast


def adjust_rms_contrast(image_stim, target_rms_contrast):
    """
    根据目标 RMS 对比度调整图像
    :param image_stim: PsychoPy 的 ImageStim 对象
    :param target_rms_contrast: 目标 RMS 对比度
    :return: 修改后的 ImageStim 对象
    """
    # 将 ImageStim 转换为 PIL 图像对象
    pil_image = image_stim.image

    # 将 PIL 图像转为 NumPy 数组
    image_array = np.array(pil_image, dtype=np.float64)

    # 归一化处理，确保数值在 [0, 1] 范围内
    image_array /= 255.0

    # 计算当前图像的 RMS 对比度
    current_rms_contrast = calculate_rms_contrast(image_array)

    # 打印当前对比度和目标对比度
    print(f"当前 RMS 对比度: {current_rms_contrast:.4f}, 目标 RMS 对比度: {target_rms_contrast:.4f}")

    # 如果当前对比度与目标对比度相差较大，进行对比度调整
    if current_rms_contrast != 0:
        # 计算调整的标准差因子
        scale_factor = target_rms_contrast / current_rms_contrast

        # 打印计算的 scale_factor
        print(f"计算得到的 scale_factor: {scale_factor:.4f}")

        # 调整图像的亮度值
        mean_value = np.mean(image_array)
        image_array = (image_array - mean_value) * scale_factor + mean_value


        # 打印调整后的对比度
        adjusted_rms_contrast = calculate_rms_contrast(image_array)
        print(f"调整后的 RMS 对比度: {adjusted_rms_contrast:.4f}")

        image_array = image_array * 255

        # 将修改后的图像转换回 PIL 图像
        pil_image = Image.fromarray(image_array.astype(np.uint8))

        # 更新 ImageStim 对象
        image_stim.image = pil_image
    else:
        print("警告: 当前图像 RMS 对比度为 0，无法调整。")

    return image_stim



def generate_noised_stimuli_with_rms_contrast(win, stimuli, target_rms_contrast_sequence):
    """
    根据目标 RMS 对比度序列修改图像刺激的对比度
    :param win: PsychoPy 的窗口对象
    :param stimuli: 原始的 ImageStim 列表
    :param target_rms_contrast_sequence: 目标 RMS 对比度序列，每个值代表目标 RMS 对比度
    :return: 修改后的图像刺激序列
    """
    # 新的刺激序列，存储修改后的 ImageStim 对象
    adjusted_stimuli = []

    # 每个对比度水平应用于 stimuli 的一部分
    num_stimuli = len(stimuli)
    num_contrasts = len(target_rms_contrast_sequence)

    # 计算每个对比度水平需要应用的刺激数量
    stimuli_per_contrast = num_stimuli // num_contrasts
    remainder = num_stimuli % num_contrasts  # 处理余数

    start_idx = 0
    for i, target_rms_contrast in enumerate(target_rms_contrast_sequence):
        # 如果是最后一个对比度水平，应用剩余的所有刺激
        end_idx = start_idx + stimuli_per_contrast + (1 if i < remainder else 0)

        # 按顺序分配每个对比度水平
        for j in range(start_idx, end_idx):
            stimulus = stimuli[j]
            adjusted_stimuli.append(adjust_rms_contrast(stimulus, target_rms_contrast))

        # 更新 start_idx 为下一个对比度应用的起始索引
        start_idx = end_idx


    print(len(stimuli))
    print(len(adjusted_stimuli))

    return adjusted_stimuli
##############################################调取法#####################################################################
def organize_stimuli(stim_dict, rms_contrast_order, stim_per_level):
    """
    组织刺激序列，根据给定的对比度顺序和每个级别的刺激数量。
    参数:
        stim_dict (dict): 包含所有对比度级别的刺激序列的字典。
        rms_contrast_order (list): RMS对比度的顺序列表。
        stim_per_level (int): 每个对比度级别需要的刺激数量。
    返回:
        list: 组织后的刺激序列。
    """
    # 初始化结果列表
    organized_stims = []

    # 计算并打印总共需要的刺激数量
    total_needed_stims = len(rms_contrast_order) * stim_per_level
    print(f"总共需要 {total_needed_stims} 张刺激。")

    # 按照给定的对比度顺序，从字典中抽取刺激
    for contrast in rms_contrast_order:
        if contrast in stim_dict:
            available_stims = len(stim_dict[contrast])  # 获取实际可用的刺激数量
            if available_stims >= stim_per_level:
                # 从对应对比度级别中选取指定数量的刺激
                selected_stims = stim_dict[contrast][:stim_per_level]
                organized_stims.extend(selected_stims)
            else:
                # 如果刺激数量不足，打印警告并选择所有可用的刺激
                print(
                    f"警告：{contrast} 对比度级别的刺激数量不足，需要 {stim_per_level} 张，实际可用 {available_stims} 张。")
                selected_stims = stim_dict[contrast][:available_stims]  # 选择所有可用的刺激
                organized_stims.extend(selected_stims)
        else:
            print(f"警告：没有找到 {contrast} 对比度级别的刺激。")

    return organized_stims







