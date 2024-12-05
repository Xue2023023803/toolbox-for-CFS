# save_data.py

import csv
import os
from datetime import datetime


def save_responses_to_csv(responses, subject_id):
    """
    保存每个试次的响应数据到CSV文件中，根据当前日期、时间和被试编号创建文件。

    参数:
    - responses: 试次响应数据的列表，每个响应包含试次号、目标点数、响应内容、响应时间
    - subject_id: 被试编号，用于命名文件
    """
    # 检查并创建 Experimental_data_results 文件夹
    folder_path = "Experimental_data_results"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 获取当前日期和时间，生成文件名
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{folder_path}/{current_time}_subject_{subject_id}.csv"

    # 打开并准备写入CSV文件
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        # 如果文件为空，则写入表头
        if file.tell() == 0:
            writer.writerow(["Trial", "Target Dots", "Response", "Response Time (s)","breakthrough_time(s)","Is Correct"])

        # 写入响应数据
        for response in responses:
            writer.writerow(response)

    print(f"数据已保存至 {filename}")
