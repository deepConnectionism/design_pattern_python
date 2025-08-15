# 运行这段代码来创建模拟数据集文件
import os
import csv

file_path = 'large_dataset.csv'
if not os.path.exists(file_path):
    print("正在创建模拟数据集...")
    with open(file_path, 'w') as f:
        f.write('feature1,feature2,label\n')
        for i in range(1000000): # 100万行数据
            f.write(f'f1_{i},f2_{i},{i%2}\n')
    print("数据集创建完成！")
else:
    print("数据集文件已存在。")

def lazy_data_loader(file_path):
    """
    一个惰性数据加载器，使用生成器按需读取数据。
    它会一次返回一行数据，而不是一次性加载整个文件。
    """
    print("数据加载器已启动...")
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader) # 跳过表头
        for row in reader:
            # 在这里可以进行一些简单的预处理
            processed_row = {
                'feature1': row[0],
                'feature2': row[1],
                'label': int(row[2])
            }
            # 使用 yield 关键字，将处理好的数据返回给调用者
            # 此时函数会暂停执行，并记住当前状态
            yield processed_row

# 客户端代码：模拟训练循环
def train_model():
    print("\n--- 开始模拟模型训练 ---")
    data_iterator = lazy_data_loader('large_dataset.csv')
    
    # 模拟训练 10 个批次的数据
    for i, data_point in enumerate(data_iterator):
        if i >= 10:
            break
        
        # 这里可以放置你的模型训练逻辑
        # 例如：model.train_on_batch(data_point['features'], data_point['label'])
        print(f"正在训练第 {i+1} 个数据点: {data_point}")
    
    print("\n--- 模拟训练完成 ---")

# 运行模拟训练
train_model()