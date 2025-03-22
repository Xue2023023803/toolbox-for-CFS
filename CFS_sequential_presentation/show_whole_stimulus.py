from psychopy import core,visual,event
from display_intro import draw_red_x
import random
import numpy as np
import math


def extend_target_sequence_by_contrast(total_duration, noise_frequency, num_contrasts, target_sequence):
    """
    根据每个对比度水平的帧数扩展目标序列。
    :param total_duration: 总时长，单位秒
    :param noise_frequency: 噪声更新频率，单位 Hz
    :param num_contrasts: 不同对比度水平的数量
    :param target_sequence: 目标刺激序列，包含每个对比度水平的一个刺激
    :return: 扩展后的目标刺激序列
    """
    frames_per_contrast = int(math.ceil((total_duration / num_contrasts) * noise_frequency))
    extended_sequence = []

    # 为每个对比度水平重复相应数量的帧
    for stim in target_sequence:
        extended_sequence.extend([stim] * frames_per_contrast)

    return extended_sequence















def present_noise_and_stimuli(win, target_sequence,line_sequence, noise_sequence, target_position, noise_position, noise_duration, noise_frequency,bloder,fusion_box_image_path):
    # 创建时钟来记录时间
    draw_red_x(win,bloder,noise_position,target_position,fusion_box_image_path,line_width=1)

    clock = core.Clock()
    frame_rate = win.getActualFrameRate()

    if frame_rate is not None:
        print("Detected frame rate:", frame_rate)
        refresh_interval = 1.0 / frame_rate
    else:
        refresh_interval = 1.0 / 60  # 默认为60Hz
        print("Using default refresh interval for 60 Hz")
    # 确保每个刺激对象都正确初始化
    for stim in target_sequence:
        if not hasattr(stim, 'draw'):
            raise TypeError("Expected visual.Stim object, got type: {}".format(type(stim)))
        stim.pos = target_position

    for noise in noise_sequence:
        if not hasattr(noise, 'draw'):
            raise TypeError("Expected visual.Stim object, got type: {}".format(type(noise)))
        noise.pos = noise_position

    # 计算每个噪声刺激之间的间隔时间，并预设一个时间点列表
    noise_intervals = [i * (1.0 / noise_frequency) for i in range(int(noise_duration * noise_frequency))]

    # 设置刺激位置
    for stim in target_sequence:
        stim.pos = target_position
    for noise in noise_sequence:
        noise.pos = noise_position


    # 初始时间戳和索引
    start_time = core.getTime()
    noise_index = 0
    first_space_time = None


    # 清空按键事件
    event.clearEvents()

    # 持续呈现，直到噪声总持续时间达到
    while core.getTime() - start_time < noise_duration:
        current_time = core.getTime()
        target_time = start_time + noise_intervals[noise_index]

        # 检测空格键按下
        keys = event.getKeys(keyList=["space"],timeStamped=clock)

        for key, time in keys:
            if key == 'space' and first_space_time is None:
                first_space_time = time
                print(f"First space key pressed at: {first_space_time:.3f} seconds")
                break  # 记录第一次按键后就不再检查

        # 检查是否到了添加噪声的时间
        if current_time >= target_time:
            if noise_index < len(noise_intervals) - 1:
                noise_index += 1
            try:
                # 绘制目标刺激和噪声刺激
                noise_sequence[noise_index].draw()
                target_sequence[noise_index].draw()
                for line in line_sequence[noise_index]:  # 遍历 line_sequence 中第 noise_index 组的每一条线
                    line.draw()  # 画出每一条线



                draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
                win.flip()  # 展示刺激

            except IndexError as e:
                print("Error presenting stimulus: index out of range", e)
                break
            except Exception as e:
                print("Error presenting stimulus:", e)
                break  # 如果出现其他错误，终止循环



        # 控制刷新间隔
        if refresh_interval > 0:
            core.wait(refresh_interval, hogCPUperiod=0.1)

    # 清理屏幕
    win.flip()

    # 返回第一次按下空格键的时间
    return first_space_time



