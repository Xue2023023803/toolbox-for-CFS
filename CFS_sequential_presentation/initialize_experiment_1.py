# initialize_experiment.py
from psychopy import visual,monitors
import os

from target.connected_dot_create import line_color


def initialize_experiment():

    # 配置显示器参数
    # 由于动态图像的运行很耗费资源，因此目前最好屏幕刷新率为60 Hz
    my_monitor = monitors.Monitor("MyMonitor", width=49, distance=27.5)  # 宽度 53cm，距离 60cm
    my_monitor.setSizePix([1920, 1080])  # 分辨率 1920x1080 像素
    # 创建主窗口
    win = visual.Window(size=(1920, 1080), monitor=my_monitor, units="pix", fullscr=True, waitBlanking=True)

    # 刺激的位置
    position_left = (-win.size[0] / 4, 0)  # 左四分之一中心
    position_right = (win.size[0] / 4, 0)  # 右四分之一中心
    bloder = [600, 600]
    fusion_box_image_path = "Fusion_Point/background/600*600.png"

########################################################################################################################

    #试验参数
    target_dots_selection = "random"  # 点阵数量选择方式 ("random" 或 "sequence")
    type_of_mission = "前后随机"    # 如果想要呈现的两个刺激随机选择 连接or不连接呈现，那么保持“前后随机”否则随意填其他值
    type_of_dots="normal"            #点阵的形式normal\connected


    line_color =[0.5,0.5,0.5]  #实际上没用的参数设定，懒得改了


    num_trials = 5  # 总的试次数量
    contrast_levels = [0.15]  # 对比度变化顺序-v
    target_dots_list = [2, 4, 6, 10, 12, 16]  # 点阵数量的候选列表
    if len(target_dots_list) != num_trials and target_dots_selection == "sequence":
        print (f"试次与点阵呈现序列不匹配,已经将试次调整为：{len(target_dots_list)}")
        num_trials = len(target_dots_list)

    SOA = 0.5    # 刺激之间的空屏时间 （秒）
    ITI = (1,2)   # 刺激呈现间隔(秒) Stimulus onset asynchrony
    timeout_duration = 1.5  # 超过此时间未反应，记录为timeout（秒）           服务于判断任务
########################################################################################################################
    # 刺激参数
    stimulus_duration = 1  # 刺激呈现时长（秒）
    least_dot_size = 25  # 单个点最小的大小
    dot_total_area = least_dot_size * max(target_dots_list)   # 点阵总面积（控制总面积一致）
    field_size = (256, 256)  # 默认的生成区域大小（宽, 高）


    #直接使用已经准备好的目标图片
    target_dir = 'target/unconnected'  # 可以根据需求修改

########################################################################################################################
    #直接使用已经准备好的掩蔽图片
    # noise_dir_path = './noise/white_noise' # 噪声图片存储位置(white_noise)
    noise_dir_path = './noise/Mondriaan-fill'  # Mondriaan-fill
    # noise_dir_path = './noise/Mondriaan-white_noise'  # Mondriaan-white_noise
    # noise_dir_path = './noise/Mondriaan-pink_noise'  # Mondriaan-pink_noise

    #掩蔽参数
    noise_stim_size = 512  # 最好为噪声生成器提供的是一个 "2的幂" 大小的纹理
    noise_duration = stimulus_duration  # 掩蔽呈现时长（秒）
    RMS_contrast = ['RMS_0.15']  # 对比度序列
    Mean_Luminance = []

    noise_frequency = 10  # 噪声频率，单位为Hz    一般是10，如果想改动这个，需要考虑呈现时，帧数控制即show_whole_stimulus.py的控制逻辑
    noise_type = 'White'  # 噪声类型 Valid types are Binary, Uniform, Normal,White, Filtered, Gabor, Isotropic or Image

    # 如果需要进行对噪声的详细操作的话
    noise_path = os.path.join(os.getcwd(), "noise")
    # 'Gaussian'高斯噪声：每个像素的亮度值符合高斯分布，产生随机波动。
    # 'Pink'粉红噪声：也称 1/f 噪声，频谱密度随频率减小而增大，常用于模拟自然界噪声。
    # 'White'白噪声：所有频率上具有均匀的功率密度，噪声表现为完全随机的亮度分布。
    # 'Uniform'均匀噪声：亮度值在指定范围内均匀分布，噪声无规律。
    # 'Multiplied'乘法噪声：基于背景图像的亮度生成噪声，噪声强度随背景变化。
    # 'SaltAndPepper'盐和胡椒噪声：像素值随机为黑或白，产生黑白斑点效果







    return win,type_of_dots,type_of_mission,line_color, num_trials, target_dots_list, target_dots_selection, noise_frequency, \
           noise_type, stimulus_duration, timeout_duration, field_size, \
           dot_total_area, noise_stim_size,position_left, position_right, contrast_levels,noise_duration,SOA,RMS_contrast,Mean_Luminance,bloder,fusion_box_image_path,noise_path,ITI,noise_dir_path,target_dir



########################################################################################################################
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
                    image_stim = visual.ImageStim(window, image=image_path)  # 创建ImageStim对象
                    image_stims.append(image_stim)  # 将ImageStim对象添加到列表中
            stim_dict[folder] = image_stims  # 将当前对比度的刺激序列添加到字典中
    return stim_dict

