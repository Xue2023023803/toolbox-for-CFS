from utils import generate_non_overlapping_positions, generate_noise_positions_from_target
from target_create import create_target_stim
from display_intro import draw_red_x
import numpy as np
from utils import generate_non_overlapping_positions,generate_connected_positions

def draw_grid_with_contrast(win, dot_size, field_size, target_position,noise_position,num_dots,bloder,fusion_box_image_path,line_color,type_of_dots,contrast_level=1):
    """
    通过调用你提供的函数绘制点阵图，设置对比度为1。
    """
    # 计算 noise_shift
    noise_shift = (noise_position[0] - target_position[0], noise_position[1] - target_position[1])
    radius = np.sqrt(dot_size / np.pi)

    ######################################################################################################################
    if type_of_dots == "connected":
        radius = np.sqrt(dot_size / np.pi)
        positions= generate_non_overlapping_positions(target_position, field_size, num_dots//2, radius*3, max_attempts=50000) #先计算每对连接点所在的“大圆位置”
        positions_target = generate_connected_positions(positions,radius, num_dots/2, max_attempts=50000) #在每个大圆中确定具体的连接点位置
        positions_noise = generate_noise_positions_from_target(positions_target,noise_shift)

    elif type_of_dots == "normal":
        radius = np.sqrt(dot_size / np.pi)
        # 计算并固定位置
        positions_target = generate_non_overlapping_positions(target_position, field_size, num_dots, radius, max_attempts=50000)
        positions_noise = generate_noise_positions_from_target(positions_target,noise_shift)

    else:
        print("type_of_dots参数没有按规定选项设定")


    # 计算并固定点的位置
    #positions_target = generate_non_overlapping_positions(target_position, field_size, num_dots, radius)
    #positions_noise = generate_noise_positions_from_target(positions_target, noise_shift )


    # 创建和呈现刺激
    dots_target,line_stim_target=create_target_stim(win, num_dots, dot_size,field_size,target_position,contrast_level, positions_target,line_color,type_of_dots)
    dots_noise,line_stim_noise=create_target_stim(win, num_dots, dot_size, field_size,target_position,contrast_level, positions_noise,line_color,type_of_dots)

    dots_noise.draw()
    dots_target.draw()
    # 遍历绘制线段（如果 line_stim 是列表）
    if isinstance(line_stim_noise, list):
        for line in line_stim_noise:
            line.draw()
    else:
        line_stim_noise.draw()  # 兼容非列表情况

    if isinstance(line_stim_target, list):
        for line in line_stim_target:
            line.draw()
    else:
        line_stim_target.draw()

    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()



def draw_grid_with_contrast_for_nromal_mission(win, dot_size, field_size, target_position,noise_position,num_dots,bloder,fusion_box_image_path,line_color,contrast_level=1):

    # 计算 noise_shift
    noise_shift = (noise_position[0] - target_position[0], noise_position[1] - target_position[1])


    # 计算并固定点的位置
    radius = np.sqrt(dot_size / np.pi)
    positions_target = generate_non_overlapping_positions(target_position, field_size, num_dots, radius)
    positions_noise = generate_noise_positions_from_target(positions_target, noise_shift )


    # 创建和呈现刺激
    dots_target,line_stim_target=create_target_stim(win, num_dots, dot_size,field_size,target_position,contrast_level, positions_target,line_color)
    dots_noise,line_stim_noise=create_target_stim(win, num_dots, dot_size, field_size,target_position,contrast_level, positions_noise,line_color)

    dots_noise.draw()
    dots_target.draw()

    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()


