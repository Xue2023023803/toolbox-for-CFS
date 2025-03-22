# display_intro.py

from psychopy import visual, event ,core

def display_intro_text(win, target_position, noise_position):
    # 创建两个TextStim对象，分别在目标位置和噪声位置显示相同的文本
    intro_text_target = visual.TextStim(win, text="欢迎你来做实验啊！！！！\n按空格键开始", color="white", height=40, pos=target_position)
    intro_text_noise = visual.TextStim(win, text="欢迎你来做实验啊！！！！\n按空格键开始", color="white", height=40, pos=noise_position)

    # 绘制两个文本
    intro_text_target.draw()
    intro_text_noise.draw()

    # 刷新窗口以显示文本
    win.flip()

    # 等待按空格键开始
    event.waitKeys(keyList=["space"])




def draw_cross(win, target_position, noise_position,fusion_box_image_path ,cross_size=25, cross_color='red', line_width=3):
    """
    在指定位置绘制两个十字形刺激。

    参数:
    - win: psychopy的窗口对象
    - target_position: 目标十字的位置 (x, y)
    - noise_position: 噪声十字的位置 (x, y)
    - cross_size: 十字的大小，默认是50
    - cross_color: 十字的颜色，默认是红色
    - line_width: 十字线条的宽度，默认是5
    """
    # 创建十字的上下左右两条线
    target_cross_vert = visual.Line(win, start=(0, -cross_size), end=(0, cross_size), lineColor=cross_color,
                                    lineWidth=line_width)
    target_cross_horiz = visual.Line(win, start=(-cross_size, 0), end=(cross_size, 0), lineColor=cross_color,
                                     lineWidth=line_width)

    noise_cross_vert = visual.Line(win, start=(0, -cross_size), end=(0, cross_size), lineColor=cross_color,
                                   lineWidth=line_width)
    noise_cross_horiz = visual.Line(win, start=(-cross_size, 0), end=(cross_size, 0), lineColor=cross_color,
                                    lineWidth=line_width)

    # 将十字放置在对应的位置
    target_cross_vert.pos = target_position
    target_cross_horiz.pos = target_position
    noise_cross_vert.pos = noise_position
    noise_cross_horiz.pos = noise_position

    # 放入融合框
    # 设置图片路径（相对路径）
    background_stim_left = visual.ImageStim(win, image=fusion_box_image_path, pos=target_position)
    background_stim_right = visual.ImageStim(win, image=fusion_box_image_path, pos=noise_position)

    # 绘制十字
    target_cross_vert.draw()
    target_cross_horiz.draw()
    noise_cross_vert.draw()
    noise_cross_horiz.draw()
    # 绘制融合框
    background_stim_right.draw()
    background_stim_left.draw()

from psychopy import visual


def draw_red_x(win, rect_size, center_pos_left, center_pos_right,fusion_box_image_path,line_width):
    # 解包矩形的长和宽
    width, height = rect_size

    # 计算矩形的左上角和右下角坐标
    half_width = width / 2
    half_height = height / 2
    top_left_left = (center_pos_left[0] - half_width, center_pos_left[1] - half_height)
    bottom_right_left = (center_pos_left[0] + half_width, center_pos_left[1] + half_height)
    top_left_right = (center_pos_right[0] - half_width, center_pos_right[1] - half_height)
    bottom_right_right = (center_pos_right[0] + half_width, center_pos_right[1] + half_height)

    # 创建两条对角线
    line1 = visual.Line(win, start=top_left_left, end=bottom_right_left, lineColor='red', lineWidth=line_width)
    line2 = visual.Line(win, start=(center_pos_left[0] - half_width, center_pos_left[1] + half_height),
                        end=(center_pos_left[0] + half_width, center_pos_left[1] - half_height), lineColor='red',
                        lineWidth=line_width)
    line3 = visual.Line(win, start=top_left_right, end=bottom_right_right, lineColor='red', lineWidth=line_width)
    line4 = visual.Line(win, start=(center_pos_right[0] - half_width, center_pos_right[1] + half_height),
                        end=(center_pos_right[0] + half_width, center_pos_right[1] - half_height), lineColor='red',
                        lineWidth=line_width)
    #融合框
    # 设置图片路径（相对路径）
    background_stim_left = visual.ImageStim(win, image=fusion_box_image_path, pos=center_pos_left)
    background_stim_right = visual.ImageStim(win, image=fusion_box_image_path, pos=center_pos_right)



    # 画出对角线
    line1.draw()
    line2.draw()
    line3.draw()
    line4.draw()
    # 绘制融合框
    background_stim_right.draw()
    background_stim_left.draw()






