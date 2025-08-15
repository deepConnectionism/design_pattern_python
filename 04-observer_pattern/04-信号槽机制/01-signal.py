from blinker import signal

# 1. 定义一个信号。我们给它一个唯一的名字 'new-best-score'。
new_best_score = signal('new-best-score')

# 2. 定义槽：一个用来处理信号的函数。
def log_result(sender, **kwargs):
    """一个槽，负责打印最好的超参数组合。"""
    print(f"日志记录: 发现新的最佳超参数组合！得分: {kwargs['score']:.4f}, 参数: {kwargs['hyperparams']}")

def save_result_to_file(sender, **kwargs):
    """另一个槽，负责将结果保存到文件中。"""
    # 模拟将结果写入文件
    print(f"文件保存: 最佳结果已写入文件。")
    # with open('best_result.txt', 'w') as f:
    #     f.write(f"得分: {kwargs['score']}\n")
    #     f.write(f"参数: {kwargs['hyperparams']}\n")

# 3. 将信号与槽连接起来。
# 'connect' 方法是核心，它将槽函数注册到信号上。
new_best_score.connect(log_result)
new_best_score.connect(save_result_to_file)

# ---

# 4. 定义一个发出信号的函数（主题）。
def run_hyperparameter_search():
    """
    模拟一个超参数搜索过程。
    当找到更好的结果时，发出信号。
    """
    print("开始超参数搜索...")
    best_score = 0
    best_params = {}

    for i in range(3):
        # 模拟搜索过程
        import random
        score = random.uniform(0.7, 0.95)
        params = {'learning_rate': 0.01 + i * 0.01, 'batch_size': 32}
        
        if score > best_score:
            best_score = score
            best_params = params
            
            # 5. 发出信号。
            # 'send' 方法用来发出信号。第一个参数是信号的发送者，
            # 后续的命名参数会传递给所有连接的槽。
            print("\n--- 找到更好的结果，发出信号！ ---")
            new_best_score.send('HyperparameterSearcher', score=best_score, hyperparams=best_params)
            print("-----------------------------------")

# 运行超参数搜索
run_hyperparameter_search()