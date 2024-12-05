from utils import generate_non_overlapping_positions, generate_noise_positions_from_target
from target_create import create_target_stim
from display_intro import draw_red_x
def draw_grid_with_contrast(win, dot_size, field_size, target_position,noise_position,num_dots,bloder,fusion_box_image_path,contrast_level=1):
    """
    通过调用你提供的函数绘制点阵图，设置对比度为1。
    """

    # 计算 noise_shift
    noise_shift = (noise_position[0] - target_position[0], noise_position[1] - target_position[1])


    # 计算并固定点的位置
    positions_target = generate_non_overlapping_positions(target_position, field_size, num_dots, dot_size)
    positions_noise = generate_noise_positions_from_target(positions_target, noise_shift )


    # 创建和呈现刺激
    dots_target=create_target_stim(win, num_dots, dot_size,field_size,target_position,contrast_level, positions_target)
    dots_noise=create_target_stim(win, num_dots, dot_size, field_size,target_position,contrast_level, positions_noise)

    dots_noise.draw()
    dots_target.draw()
    draw_red_x(win,bloder,target_position,noise_position,fusion_box_image_path,line_width=1)
    win.flip()

