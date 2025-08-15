from blinker import signal

# 定义一个信号
training_update = signal('training-update')

# 定义一个处理信号的槽（函数）
def log_training_status(sender, **kw):
    print(f"Log: 训练状态已更新。最新准确率: {kw['accuracy']:.2f}")

# 将信号与槽连接起来
training_update.connect(log_training_status)

# 模拟训练
def run_training():
    # 模拟训练过程...
    accuracy = 0.95
    # 发出信号，附带数据
    training_update.send('TrainingMonitor', accuracy=accuracy)

# 运行训练，会自动触发槽
run_training()