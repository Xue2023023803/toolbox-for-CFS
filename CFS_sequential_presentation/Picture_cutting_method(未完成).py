import os
from psychopy import visual, core
from PIL import Image, ImageEnhance


def enhance_and_display_images(win, contrast_levels, stimulus_folder, pos=[0, 0]):
    # 验证刺激材料文件夹是否存在
    if not os.path.exists(stimulus_folder) or not os.listdir(stimulus_folder):
        print("指定的文件夹不存在或为空。")
        return

    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(stimulus_folder) if f.endswith('.png') or f.endswith('.jpg')]

    # 遍历所有图片文件并调整对比度
    for image_file in image_files:
        # 读取图片
        img_path = os.path.join(stimulus_folder, image_file)
        try:
            img = Image.open(img_path)
        except IOError:
            print(f"无法打开图像文件：{img_path}")
            continue

        for contrast in contrast_levels:
            # 调整对比度
            enhancer = ImageEnhance.Contrast(img)
            enhanced_img = enhancer.enhance(contrast)
            # 归一化
            enhanced_img = enhanced_img.point(lambda p: p / 255.0)
            # 将图像保存为临时文件（可选）
            temp_path = 'temp_enhanced_image.png'
            enhanced_img.save(temp_path)
            # 创建Psychopy的ImageStim对象（用作纹理）
            stim = visual.ImageStim(win, image=temp_path, pos=pos)


            # 显示图像，持续一定时间
            stim.draw()
            win.flip()
            core.wait(1)  # 显示1秒，按需调整

        # 删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)



# 设定对比度序列
contrast_levels = [1, 5, 11]  # 可以调整此列表的值
stimulus_folder = 'stimulus_material'  # 假设图片存放在同目录下的文件夹

# 调用函数
enhance_and_display_images(contrast_levels, stimulus_folder, pos=[100, 100])