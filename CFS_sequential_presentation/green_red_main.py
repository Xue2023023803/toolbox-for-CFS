# green_red_main.py
from psychopy import visual, core, event
from save_data import save_responses_to_csv
from utils_2 import collect_subject_info ,fusion_point
import matplotlib.pyplot as plt
import os
from PIL import Image
import numpy as np
from Entropy_stepwise_method import calculate_entropy,entropy_adjust_contrast,sample_adjust_contrast
from green_red_trail_run import run_trial
from display_intro import display_intro_text ,draw_red_x
from noise_create import process_noise_stimuli
from  target_create import process_target_stimuli

from initialize_experiment import initialize_experiment


def load_and_create_stimuli(folder_path, win):
    """
    加载指定文件夹下每个子文件夹中的图片文件，处理图像并创建视觉刺激对象。
    :param folder_path: 主文件夹路径，其中包含若干子文件夹
    :param win: psychopy窗口对象，用于展示图片
    :return: 一个字典，键是子文件夹名称，值是该文件夹中的视觉刺激对象序列
    """
    stim_objects_dict = {}

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
                    try:
                        # 加载原始图像
                        pil_image = Image.open(file_path)

                        # 获取原始图片的尺寸 (宽度, 高度)
                        original_size = pil_image.size

                        print(original_size)

                        # 转换为灰度图像并转换为RGB三通道
                        pil_image_gray = pil_image.convert('L')
                        rgb_image = np.stack([np.array(pil_image_gray)] * 3, axis=-1)

                        # 归一化到 [0, 1] 范围
                        rgb_image = rgb_image / 255.0  # 将像素值归一化到 [0, 1]


                        # 创建ImageStim对象，并保持原始图像尺寸
                        stim = visual.ImageStim(win, image=rgb_image,size=original_size)
                        stimuli_list.append(stim)  # 将ImageStim对象添加到列表中

                    except Exception as e:
                        print(f"加载图像 {file} 时出错: {e}")

            # 将该子文件夹的刺激序列存储到字典中
            if stimuli_list:
                stim_objects_dict[subfolder] = stimuli_list

    return stim_objects_dict


def load_and_create_stims(base_path, window):
    """
    从以'RMS_'开头的文件夹中加载所有图片，并创建ImageStim对象。
    参数:
        base_path (str): 包含RMS文件夹的目录路径。
        window: 用于创建ImageStim的PsychoPy窗口对象。
    返回:
        dict: 键为文件夹名的ImageStim对象列表的字典。
    """
    stim_dict = {}  # 创建一个空字典用来存储刺激序列
    for folder in sorted(os.listdir(base_path)):
        if folder.startswith('RMS_'):  # 确认文件夹名以'RMS_'开头
            folder_path = os.path.join(base_path, folder)
            image_stims = []  # 创建一个列表用来存储当前文件夹下的所有ImageStim对象
            for image in sorted(os.listdir(folder_path)):
                image_path = os.path.join(folder_path, image)
                if image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):  # 确认文件是图片格式
                    # 加载图片并转换为灰度图
                    pil_image = Image.open(image_path).convert('L')  # 'L'表示灰度模式
                    # 将灰度图转换为三通道图像
                    rgb_image = np.stack([np.array(pil_image)] * 3, axis=-1)
                    # 归一化到[0, 1]范围
                    rgb_image = rgb_image / 255.0  # 将像素值归一化到 [0, 1]


                    # 获取原始图片的尺寸
                    pil_image = Image.open(image_path)
                    original_size = pil_image.size  # 原图尺寸 (width, height)

                    # 创建ImageStim对象，强制指定大小为原始图像的尺寸
                    processed_image = visual.ImageStim(window, image=rgb_image, size=original_size)
                    image_stims.append(processed_image)  # 将ImageStim对象添加到列表中

            stim_dict[folder] = image_stims  # 将当前对比度的刺激序列添加到字典中
    return stim_dict





########################################################################################################################
def main():
    win, num_trials, target_dots_list, target_dots_selection, noise_frequency, \
    noise_type, stimulus_duration, timeout_duration, field_size, \
    dot_total_area, noise_stim_size, position_left, position_right, contrast_levels, noise_duration,SOA,RMS_contrast,Mean_Luminance,bloder,fusion_box_image_path,noise_path,ITI,noise_dir_path,target_dir = initialize_experiment()


    correct_responses = 0
    incorrect_responses = 0

    # 加载target图像刺激
    # 创建刺激序列
    stim_objects_dict = load_and_create_stimuli(target_dir,win)


    stim_objects_dict = process_target_stimuli(stim_objects_dict,channel="G")


    # 加载noise图像刺激
    noise_all_stims = load_and_create_stims(noise_dir_path, win)
    # 例如，只保留红色通道（R）
    noise_all_stims = process_noise_stimuli(noise_all_stims, channel='R')

    # 打印每个对比度级别加载的图像数量
    for contrast_level, stims in noise_all_stims.items():
        print(f"{contrast_level}: {len(stims)} 张图片已加载。")


###################################################被试信息收集部分########################################################

    #subject_name, subject_id = collect_subject_info(win, position_left, position_right)
    responses = []
    # 初始化连续正确和错误计数
    correct_count = 0
    incorrect_count = 0
    position_center=[0,0]

    position_left = position_center
    position_right = position_center


    display_intro_text(win,position_left,position_right)

    # 优势眼测试                     眼镜：左绿右红
    strong_eye = 1               # 1=left,2=right
    if strong_eye ==1:
        target_position = position_right
        noise_position = position_left
        noise_color = "G"
        target_color ="R"

    else:
        target_position =position_left
        noise_position = position_right
        noise_color = "R"
        target_color = "G"


##########################################BLOCK设计######################################################################
    ###block1(CFS+点阵+数量比较）
    for trial in range(num_trials):
        print(f"开始第 {trial + 1} 次试验")  # 输出调试信息
        trial_responses = run_trial(win, trial, target_dots_list, target_dots_selection, stimulus_duration,
                                    timeout_duration, noise_frequency, noise_type, target_position,
                                    noise_position, field_size, dot_total_area,noise_stim_size,contrast_levels,noise_duration,SOA,bloder,RMS_contrast,fusion_box_image_path,noise_path,noise_all_stims,ITI,stim_objects_dict)
        responses.extend(trial_responses)

        # 遍历每个试次的响应数据
        for i,response_data in enumerate(trial_responses):
            trial_number, num_dots, response, response_time, breakthrough_time = response_data

            # 计算是否正确
            target_response = "num_5" if num_dots - 15 > 0 else "s"  # 根据 num_dots 判断正确响应
            if response == target_response:
                correct_responses += 1
                is_correct = True
                print("T")
            else:
                incorrect_responses += 1
                is_correct = False
                print("F")


            # 在原有数据中添加“是否正确”标志
            updated_response_data = (*response_data, is_correct)  # 在元组末尾添加 `is_correct`

            # 更新 trial_responses 中对应位置的元素
            trial_responses[i] = updated_response_data
            responses.extend(trial_responses)  # 添加每个试次的数据到 responses 中

            # 计算当前试次的成功率
            total_responses = correct_responses + incorrect_responses
            p = correct_responses / total_responses if total_responses > 0 else 0.5  # 避免除以零


        # 最后计算并打印总体正确率
        final_accuracy = correct_responses / num_trials
        print(f"最终准确率: {final_accuracy}")





###################################################保存数据###############################################################


    #save_responses_to_csv(responses,subject_id)
    win.close()




if __name__ == "__main__":
    main()
