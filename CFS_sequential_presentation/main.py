# main.py
from psychopy import visual, core, event
from save_data import save_responses_to_csv
from utils import collect_subject_info ,fusion_point
import matplotlib.pyplot as plt
import os
import pandas as pd
from Entropy_stepwise_method import calculate_entropy,entropy_adjust_contrast,sample_adjust_contrast
from run_trial import run_trial
from display_intro import display_intro_text ,draw_red_x
from  target_create import load_image_stimuli,create_stimulus_sequence
#######################################################修改处#####################################################################
from initialize_experiment import initialize_experiment,load_and_create_stims
#from initialize_experiment_1 import initialize_experiment,load_and_create_stims
#################################################################################################################################
#from debugging_initialize_experiment import initialize_experiment,load_and_create_stims


def main():
    win,type_of_dots,type_of_mission,line_color, num_trials, target_dots_list, target_dots_selection, noise_frequency, \
    noise_type, stimulus_duration, timeout_duration, field_size, \
    dot_total_area, noise_stim_size, position_left, position_right, contrast_levels, noise_duration,SOA,RMS_contrast,Mean_Luminance,bloder ,fusion_box_image_path,noise_path,ITI,noise_dir_path,target_dir = initialize_experiment()

    correct_responses = 0
    incorrect_responses = 0

    # 加载target图像刺激
    # 加载目标文件夹下的图片路径
    stimuli_dict = load_image_stimuli(target_dir)
    # 创建刺激序列
    stim_objects_dict = create_stimulus_sequence(win, stimuli_dict)

    # 加载noise图像刺激
    noise_all_stims = load_and_create_stims(noise_dir_path, win)

    # 打印每个对比度级别加载的图像数量
    for contrast_level, stims in noise_all_stims.items():
        print(f"{contrast_level}: {len(stims)} 张图片已加载。")


###################################################被试信息收集部分########################################################
    dominant_eye = "左眼"
    subject_name, subject_id,dominant_eye = collect_subject_info(win, position_left, position_right)
    responses = []
    # 初始化连续正确和错误计数
    correct_count = 0
    incorrect_count = 0


    display_intro_text(win,position_left,position_right)

    # 优势眼测试
    if dominant_eye =="左眼":    # 1=left,2=right
        target_position = position_right
        noise_position = position_left
    else:
        target_position =position_left
        noise_position = position_right


##########################################BLOCK设计######################################################################
    block = 2

    if block == 1:
        ####block1(CFS+点阵+数量比较） 对比度前测

        for trial in range(num_trials):
            print(f"开始第 {trial + 1} 次试验")  # 输出调试信息
            #trial_responses = run_trial(win, trial, target_dots_list, target_dots_selection, stimulus_duration,timeout_duration, noise_frequency, noise_type, target_position,noise_position, field_size, dot_total_area,noise_stim_size,contrast_levels,noise_duration,SOA,bloder,RMS_contrast,fusion_box_image_path,noise_path,noise_all_stims,ITI,stim_objects_dict)
            # 修改 block1 的调用如下：
            trial_responses = run_trial(
                win,
                type_of_dots,  # 添加缺失的参数
                line_color,  # 添加缺失的参数
                trial,
                target_dots_list,
                target_dots_selection,
                stimulus_duration,
                timeout_duration,
                noise_frequency,
                noise_type,
                target_position,
                noise_position,
                field_size,
                dot_total_area,
                noise_stim_size,
                contrast_levels,
                noise_duration,
                SOA,
                bloder,
                RMS_contrast,
                fusion_box_image_path,
                noise_path,
                noise_all_stims,
                ITI,  # 确保参数顺序正确
                stim_objects_dict  # 确保参数顺序正确
            )
            responses.extend(trial_responses)


            # 遍历每个试次的响应数据
            for response_data in trial_responses:
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

        # 计算熵值并调控下一个trail的noise刺激强度
                # 计算当前试次的成功率
                total_responses = correct_responses + incorrect_responses
                p = correct_responses / total_responses if total_responses > 0 else 0.5  # 避免除以零

                # 计算熵值
                entropy = calculate_entropy(p)
                print(f"第 {trial_number} 次试验的熵值: {entropy}")



                # 根据熵值调整对比度
                #RMS_contrast[0], current_index =entropy_adjust_contrast(entropy, RMS_contrast[0])


                # 根据连续的按键正确性来调整对比度

                RMS_contrast[0], correct_count, incorrect_count = sample_adjust_contrast(is_correct, RMS_contrast[0],correct_count, incorrect_count)
                print(f"Updated Contrast: {RMS_contrast[0]}")



        # 最后计算并打印总体正确率
        final_accuracy = correct_responses / num_trials
        print(f"最终准确率: {final_accuracy}")



    elif block==2 :
        ###block2(CFS+点阵+数量比较）
        for trial in range(num_trials):
            print(f"开始第 {trial + 1} 次试验")  # 输出调试信息
            trial_responses = run_trial(win,type_of_dots,type_of_mission,line_color, trial, target_dots_list, target_dots_selection, stimulus_duration,
                                        timeout_duration, noise_frequency, noise_type, target_position,
                                        noise_position, field_size, dot_total_area,noise_stim_size,contrast_levels,noise_duration,SOA,bloder,RMS_contrast,fusion_box_image_path,noise_path,noise_all_stims,ITI,stim_objects_dict)
            #responses.extend(trial_responses)

            # 遍历每个试次的响应数据
            updated_trial_data = []
            for i,response_data in enumerate(trial_responses):
                trial_number, num_dots, response, response_time, breakthrough_time,before_type_of_dots = response_data

                if before_type_of_dots == "connected":
                    connected_before_or_after="连接点在前"
                    print(connected_before_or_after)
                elif before_type_of_dots == "normal":
                    connected_before_or_after = "连接点在后"
                    print(connected_before_or_after)
                else:
                    print("没有正确记录连接点出现位置")

                # 计算是否正确
                target_response = "num_5" if num_dots - 8 > 0 else "s"  # 根据 num_dots 判断正确响应
                if response == target_response:
                    correct_responses += 1
                    is_correct = True
                    print("T")
                else:
                    incorrect_responses += 1
                    is_correct = False
                    print("F")

                # 构建完整数据条目（一次性添加所有字段）
                full_data = (
                    trial_number,
                    num_dots,
                    response,
                    response_time,
                    breakthrough_time,
                    before_type_of_dots,
                    is_correct,
                    connected_before_or_after
                )
                updated_trial_data.append(full_data)

                # 将完整数据添加到总列表（每个试次只添加一次）
                responses.extend(updated_trial_data)

                # 计算当前试次的成功率
                total_responses = correct_responses + incorrect_responses
                p = correct_responses / total_responses if total_responses > 0 else 0.5  # 避免除以零


        # 最后计算并打印总体正确率
        final_accuracy = correct_responses / num_trials
        print(f"最终准确率: {final_accuracy}")




###################################################保存数据###############################################################


    save_responses_to_csv(responses,subject_id)
    win.close()



if __name__ == "__main__":
    main()
