import psychopy
from psychopy import core,event,visual
import random
import numpy as np
from PIL import Image
from utils_2 import validate_field_size_and_dot_size
from target_create import generate_stimulus_sequence,create_target_sequence,generate_stimulus_sequence
from noise_create import create_noise_sequence,create_psychopy_stimulus,generate_noised_stimuli_with_rms_contrast,organize_stimuli
from display_intro import draw_red_x
from quantitative_comparison import draw_grid_with_contrast
from show_whole_stimulus import present_noise_and_stimuli, extend_target_sequence_by_contrast







def create_fused_stimuli_sequence(stimuli_sequence_1, stimuli_sequence_2, win):
    """
    将两个刺激序列的图像按照RGB通道融合，生成新的刺激序列。
    将较小的图像放置在较大图像的中心，并融合其RGB通道。

    参数：
    stimuli_sequence_1 (list): 第一个刺激序列，包含ImageStim对象。
    stimuli_sequence_2 (list): 第二个刺激序列，包含ImageStim对象。
    win (psychopy.visual.Window): Psychopy窗口，用于创建ImageStim对象。

    返回：
    new_stimuli_sequence (list): 融合后的新刺激序列，包含ImageStim对象。
    """
    new_stimuli_sequence = []

    for stim1, stim2 in zip(stimuli_sequence_1, stimuli_sequence_2):
        # 获取图像的numpy数组
        img_array1 = stim1.image  # 直接获取ImageStim的numpy数组
        img_array2 = stim2.image  # 直接获取ImageStim的numpy数组

        # 确保图像是RGBA格式（如果是RGB图像，可以转换成RGBA）
        if img_array1.shape[2] == 3:  # 如果是RGB
            img_array1 = np.concatenate([img_array1, np.ones((img_array1.shape[0], img_array1.shape[1], 1), dtype=np.uint8) * 255], axis=2)
        if img_array2.shape[2] == 3:  # 如果是RGB
            img_array2 = np.concatenate([img_array2, np.ones((img_array2.shape[0], img_array2.shape[1], 1), dtype=np.uint8) * 255], axis=2)

        # 确保数据类型为uint8
        img_array1 = img_array1.astype(np.uint8)
        img_array2 = img_array2.astype(np.uint8)

        # 获取两个图像的尺寸
        height1, width1 = img_array1.shape[:2]
        height2, width2 = img_array2.shape[:2]

        # 创建一个新的透明背景图像 (RGBA)
        new_height = max(height1, height2)
        new_width = max(width1, width2)
        new_img = Image.new('RGBA', (new_width, new_height), (255, 255, 255, 0))  # 白色透明背景

        # 将第二个图像放置到第一个图像中心
        top_left_x = (new_width - width2) // 2
        top_left_y = (new_height - height2) // 2

        # 将img_array1和img_array2转换为PIL图像
        img1_pil = Image.fromarray(img_array1)
        img2_pil = Image.fromarray(img_array2)

        # 将第二个图像img2_pil粘贴到新图像的中央，保持透明通道
        new_img.paste(img2_pil, (top_left_x, top_left_y), img2_pil.convert('RGBA'))

        # 将第一个图像img1_pil粘贴到新图像上，保持透明通道
        new_img.paste(img1_pil, (0, 0), img1_pil.convert('RGBA'))

        # 将新图像转换回numpy数组
        new_img_array = np.array(new_img)

        # 将新的图像（numpy数组）转换为ImageStim对象
        new_stimuli = visual.ImageStim(win, image=new_img_array)

        # 将新的ImageStim对象添加到刺激序列
        new_stimuli_sequence.append(new_stimuli)

    return new_stimuli_sequence








########################################################################################################################
def run_trial(win, trial, num_dots_list, target_dots_selection, stimulus_duration, timeout_duration,
              noise_frequency, noise_type, target_position, noise_position, field_size,
              dot_total_area, noise_stim_size, contrast_levels,noise_duration,SOA,bloder,RMS_contrast,fusion_box_image_path,noise_path,noise_all_stims,ITI,stim_objects_dict):


    responses = []
    iti = random.uniform(ITI[0],ITI[1])


###############################################目标刺激加载###############################################################
    # 随机选择点阵的数量
    if target_dots_selection == "random":
        num_dots = random.choice(num_dots_list)
    elif target_dots_selection == "sequence":
        num_dots = num_dots_list[trial]
    dot_size = dot_total_area / num_dots

    # 验证点阵参数
    validate_field_size_and_dot_size(field_size, dot_size, num_dots)


    #################################################创建刺激（点阵）######################################################
    # 创建目标刺激序列
    #stimulus_sequence = generate_stimulus_sequence(win, num_dots, dot_size, field_size, target_position,contrast_levels, stimulus_duration)

    # 解包：stimulus_sequence 包含字典，你需要传递给需要 visual.Stim 对象的函数
    #target_sequence = [item['stimulus'] for item in stimulus_sequence]  # 提取所有的 visual.Stim 对象


    ###################################################使用准备好的目标刺激#################################################
    # 创建目标刺激序列
    target_sequence = create_target_sequence(stim_objects_dict, contrast_levels, num_dots, len(contrast_levels),target_size=field_size)



################################################噪音刺激加载（三选一）##############################################################
    # 创建噪声刺激
    #noise_stim = create_noise_sequence(win, noise_stim_size, noise_type, noise_position,noise_frequency,noise_duration) #可以选定方法
    # 读取噪声
    #noise_stim = create_psychopy_stimulus(win,stimulus_duration,noise_position,noise_stim_size,noise_path)    # 简单方法

    # 噪音处理（空间）
    #noise_stim=generate_noised_stimuli_with_rms_contrast(win,noise_stim,RMS_contrast)
    #对空间频率进行滤波

    # 使用已经准备好的掩蔽图片
    # 按照RMS_contrast的顺序来呈现刺激
    stim_per_level = int(noise_duration * noise_frequency / len(RMS_contrast))


    noise_stim = organize_stimuli(noise_all_stims, RMS_contrast, stim_per_level)




    ########################################################################################################################

    noise_sequence =noise_stim

    # 对齐target和noise的帧数
    target_sequence=extend_target_sequence_by_contrast(stimulus_duration,noise_frequency,len(contrast_levels),target_sequence)




    # 形成红绿融合图像
    target_sequence =create_fused_stimuli_sequence(noise_sequence,target_sequence,win)
    noise_sequence = create_fused_stimuli_sequence(noise_sequence,target_sequence,win)


################################################################################################################################################################
    # 绘制十字注意点
    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()
    core.wait(iti)

    # 同步绘制目标刺激和噪声刺激
    breakthrough_time = present_noise_and_stimuli(win, target_sequence,noise_sequence,target_position,noise_position, noise_duration, noise_frequency,bloder,fusion_box_image_path)

    #SOA空屏
    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()
    core.wait(SOA)

    # 判断任务
    # 记录开始时间
    target_start_time = core.getTime()
    # 刺激呈现
    special_dot_num = 7   ## 注意！！！：按照具体的设计决定
    special_dot_size = dot_total_area / special_dot_num

    draw_grid_with_contrast(win, special_dot_size, field_size, target_position,noise_position,special_dot_num ,bloder,fusion_box_image_path,contrast_level=0.15)


    # 等待按键反应
    keys = event.waitKeys(maxWait=timeout_duration, keyList=["s", "num_5"])

    # 记录反应时间
    response_time = core.getTime() - target_start_time

    # 如果没有按键（超时）
    if keys is None:
        response = "timeout"
        response_time = timeout_duration
    else:
        # 如果按下了某个键，记录该键作为响应
        response = keys[0]

    # 记录响应时间
    responses.append((trial + 1, num_dots, response, response_time,breakthrough_time))


    # 在记录完响应后，等待空格键 （B-CFS范式使用）
    # 如果按下了空格键，标记进入下一个试验
    #while True:
        #keys = event.waitKeys(keyList=["space"])  # 只监听空格键
        #if "space" in keys:
            #return responses

    return responses  # 进入下一个试验


