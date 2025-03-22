from numpy.f2py.crackfortran import beforethisafter
from psychopy import core, event
import random
from utils import validate_field_size_and_dot_size
from target_create import generate_stimulus_sequence,create_target_sequence
from noise_create import create_noise_sequence,create_psychopy_stimulus,generate_noised_stimuli_with_rms_contrast,organize_stimuli
from display_intro import draw_red_x
from quantitative_comparison import draw_grid_with_contrast, draw_grid_with_contrast_for_nromal_mission
from show_whole_stimulus import present_noise_and_stimuli, extend_target_sequence_by_contrast

def run_trial(win,type_of_dots,type_of_mission, line_color,trial, num_dots_list, target_dots_selection, stimulus_duration, timeout_duration,
              noise_frequency, noise_type, target_position, noise_position, field_size,
              dot_total_area, noise_stim_size, contrast_levels,noise_duration,SOA,bloder,RMS_contrast,fusion_box_image_path,noise_path,noise_all_stims,ITI,stim_objects_dict):


    responses = []
    iti = random.uniform(ITI[0],ITI[1])

    if type_of_mission == "前后随机":
        value1 = "normal"
        value2 = "connected"
        # 将两个值放入列表
        options = [value1, value2]
        # 随机选择一个值
        before_type_of_dots= random.choice(options)
        # 找到未被选中的值
        if before_type_of_dots == value1:
            after_type_of_dots = value2
        else:
            after_type_of_dots = value1
        print("随机选择的结果是:", before_type_of_dots)
    else:
        before_type_of_dots = type_of_dots


###############################################目标刺激加载###############################################################
    # 随机选择点阵的数量
    if target_dots_selection == "random":
        num_dots = random.choice(num_dots_list)
    elif target_dots_selection == "sequence":
        num_dots = num_dots_list[trial]
    dot_size = dot_total_area / num_dots  #每个点的面积



    #if type_of_dots == "normal":
         #验证点阵参数
        #validate_field_size_and_dot_size(field_size, dot_size, num_dots)
    #elif type_of_dots == "connected":
        #validate_field_size_and_dot_size(field_size,dot_size*4,num_dots)



    #################################################创建刺激（点阵）######################################################
    # 创建目标刺激序列
    stimulus_sequence = generate_stimulus_sequence(win, num_dots, dot_size, field_size, target_position,contrast_levels, stimulus_duration,before_type_of_dots,line_color)
    # 解包：stimulus_sequence 包含字典，你需要传递给需要 visual.Stim 对象的函数
    target_sequence = [item['stimulus'] for item in stimulus_sequence]  # 提取所有的 visual.Stim 对象
    line_sequence = [item['line_stimulus'] for item in stimulus_sequence]


    ###################################################使用准备好的目标刺激#################################################
    # 创建目标刺激序列
    #target_sequence = create_target_sequence(stim_objects_dict, contrast_levels, num_dots, len(contrast_levels),field_size)



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
    line_sequence = extend_target_sequence_by_contrast(stimulus_duration,noise_frequency,len(contrast_levels),line_sequence)

################################################################################################################################################################
    # 绘制十字注意点
    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()
    core.wait(iti)

    # 同步绘制目标刺激和噪声刺激
    breakthrough_time = present_noise_and_stimuli(win, target_sequence,line_sequence,noise_sequence,target_position,noise_position, noise_duration, noise_frequency,bloder,fusion_box_image_path)

    #SOA空屏
    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()
    core.wait(SOA)

    # 判断任务
    # 记录开始时间
    target_start_time = core.getTime()
    # 刺激呈现
    special_dot_num = 8   ## 注意！！！：按照具体的设计决定
    special_dot_size = dot_total_area / special_dot_num
##############################################判断任务内容（二选一）########################################################
    if type_of_mission == "前后随机":
        if before_type_of_dots == "normal":
            # 固定点数
            draw_grid_with_contrast(win, dot_size, field_size, target_position, noise_position, num_dots,
                                    bloder, fusion_box_image_path, line_color,after_type_of_dots, contrast_level=0.15)
            # 双随机                       如果启用这个方法计算部分也需要更改，还没有进行呢
            # num_dots = random.choice(num_dots_list)
            # dot_size = dot_total_area / num_dots  # 每个点的面积
            # draw_grid_with_contrast(win, dot_size, field_size, target_position,noise_position,num_dots ,bloder,fusion_box_image_path,line_color,contrast_level=0.15)
        elif before_type_of_dots == "connected":
            # 与CFS的数量一致
            draw_grid_with_contrast(win, dot_size, field_size, target_position, noise_position, num_dots, bloder,
                                    fusion_box_image_path, line_color,after_type_of_dots,contrast_level=0.15)
        else:
            print("判断内容设置错误")

    else:
        if type_of_dots == "normal":
            # 固定点数
            draw_grid_with_contrast_for_nromal_mission(win, special_dot_size, field_size, target_position,noise_position,special_dot_num ,bloder,fusion_box_image_path,line_color,contrast_level=0.15)
            # 双随机                       如果启用这个方法计算部分也需要更改，还没有进行呢
            #num_dots = random.choice(num_dots_list)
            #dot_size = dot_total_area / num_dots  # 每个点的面积
            #draw_grid_with_contrast(win, dot_size, field_size, target_position,noise_position,num_dots ,bloder,fusion_box_image_path,line_color,contrast_level=0.15)
        elif type_of_dots == "connected":

            #与CFS的数量一致
            draw_grid_with_contrast_for_nromal_mission(win,dot_size,field_size,target_position, noise_position, num_dots, bloder, fusion_box_image_path, line_color,contrast_level=0.15)
        else :
            print("判断内容设置错误")

########################################################################################################################
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
    responses.append((trial + 1, num_dots, response, response_time,breakthrough_time,before_type_of_dots))


    # 在记录完响应后，等待空格键 （B-CFS范式使用）
    # 如果按下了空格键，标记进入下一个试验
    #while True:
        #keys = event.waitKeys(keyList=["space"])  # 只监听空格键
        #if "space" in keys:
            #return responses

    return responses  # 进入下一个试验


