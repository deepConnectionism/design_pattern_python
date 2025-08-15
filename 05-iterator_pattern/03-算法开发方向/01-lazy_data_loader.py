import time
import os

def lazy_data_loader(file_path):
    """一个模拟惰性加载大文件的生成器。"""
    print("开始加载数据...")
    with open(file_path, 'r') as f:
        for line in f:
            # 模拟数据预处理
            processed_data = line.strip().upper()
            yield processed_data
            # time.sleep(0.1) # 模拟处理耗时

# 假设你有一个名为 'big_data.txt' 的大文件
with open('big_data.txt', 'w') as f:
    for i in range(1000000):
        f.write(f"data_item_{i}\n")

# 使用惰性加载器
print("开始训练，使用惰性加载器...")
for data in lazy_data_loader('big_data.txt'):
    # 这里是你的模型训练代码，每次只处理一行数据
    # print(data)
    pass
print("训练完成。")