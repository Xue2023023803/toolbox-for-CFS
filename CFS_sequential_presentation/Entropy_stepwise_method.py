import math
contrast_levels = ['RMS_0.05', 'RMS_0.15', 'RMS_0.25', 'RMS_0.35', 'RMS_0.45']


# 计算熵值的函数
def calculate_entropy(p):
    if p == 0 or p == 1:
        return 0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
# 计算并调整对比度的函数
def entropy_adjust_contrast(entropy, current_contrast):
    # 获取当前对比度的索引
    current_index = contrast_levels.index(current_contrast)

    # 根据熵值来决定是否增加或减少对比度
    entropy_threshold_high = 0.70  # 熵值较高时，增加强度
    entropy_threshold_low = 0.30  # 熵值较低时，减少强度

    if entropy > entropy_threshold_high:
        # 熵较大，增加对比度
        if current_index < len(contrast_levels) - 1:
            current_index += 1  # 提高强度
    elif entropy < entropy_threshold_low:
        # 熵较小，减少对比度
        if current_index > 0:
            current_index -= 1  # 降低强度

    # 返回新的对比度（作为字符串）和当前索引
    return contrast_levels[current_index], current_index


########################################################################################################################
# 计算并调整对比度的函数
def sample_adjust_contrast(is_correct, current_contrast, correct_count, incorrect_count):
    # 获取当前对比度的索引
    current_index = contrast_levels.index(current_contrast)

    # 反馈正确或错误，根据正确/错误计数调整对比度
    if is_correct:
        correct_count += 1  # 正确计数增加
        incorrect_count = 0  # 错误计数重置
    else:
        incorrect_count += 1  # 错误计数增加
        correct_count = 0  # 正确计数重置

    # 连续 3 次正确，则提高对比度
    if correct_count >= 3:
        if current_index < len(contrast_levels) - 1:
            current_index += 1  # 提高对比度
            print("连续三次正确，提高高！！！！")
        correct_count = 0  # 重置连续正确计数


    # 连续 3 次错误，则降低对比度
    elif incorrect_count >= 3:
        if current_index > 0:
            current_index -= 1  # 降低对比度
        incorrect_count = 0  # 重置连续错误计数
        print("连续三次错误，降低低")


    # 返回新的对比度（作为字符串）和当前索引，以及更新的计数器
    return contrast_levels[current_index], correct_count, incorrect_count



