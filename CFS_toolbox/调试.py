from psychopy import visual, core, event
import os
from initialize_experiment import initialize_experiment

win, num_trials, target_dots_list, target_dots_selection, noise_frequency, \
    noise_type, stimulus_duration, timeout_duration, field_size, \
    dot_total_area, noise_stim_size, position_left, position_right, contrast_levels, noise_duration, SOA, RMS_contrast, Mean_Luminance, bloder, fusion_box_image_path, noise_path, ITI = initialize_experiment()


target_position =position_left
noise_position = position_right


# 设置图像文件夹路径
image_folder_path = 'Fusion_Point'  # 请替换为你的图像文件夹路径
background_folder_path = os.path.join(image_folder_path, 'background')  # 边框图像所在的子文件夹路径

# 获取图像文件夹中的所有图像文件路径（目标图像）
image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
# 获取background文件夹中的所有图像文件路径（边框图像）
image_border_files = [os.path.join(background_folder_path, f) for f in os.listdir(background_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# 确保图像文件夹中只有一个图像文件，background文件夹中只有一个边框图像
if len(image_files) == 1 and len(image_border_files) == 1:
    image_file = image_files[0]  # 获取目标图像文件的路径
    image_border = image_border_files[0]  # 获取边框图像文件的路径
else:
    print("文件夹中存在多个图片, 需要删除多余图片(只保留融合点和边框图像)")
    core.quit()  # 退出程序，避免继续执行

# 加载图像并创建ImageStim对象
image_stim_left = visual.ImageStim(win, image=image_file, pos=target_position)
image_stim_right = visual.ImageStim(win,image=image_file,pos= noise_position)
image_border_left = visual.ImageStim(win, image=image_border, pos=target_position)
image_border_right =visual.ImageStim(win, image=image_border, pos=noise_position)
# 显示图像
image_stim_left.draw()
image_stim_right.draw()
image_border_left.draw()
image_border_right.draw()

win.flip()

while True:
    keys = event.waitKeys(keyList=['space'], timeStamped=True)
    if keys:  # 如果有按键被按下
        win.flip()  # 刷新窗口
        # 可以在这里添加其他需要在空格键按下时执行的代码
        break  # 如果需要在按下一次空格键后退出循环，可以取消注释这行


# 获取并打印图像的长宽(调试用)
#width, height = image_stim_left.size
#print(f"Image {os.path.basename(image_file)} dimensions: {width} x {height}")

core.quit()


