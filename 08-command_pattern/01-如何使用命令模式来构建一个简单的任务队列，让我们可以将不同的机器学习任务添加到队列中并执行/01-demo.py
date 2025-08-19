from abc import ABC, abstractmethod

# 抽象命令接口
class Task(ABC):
    """所有命令（任务）都必须实现的接口。"""
    @abstractmethod
    def execute(self):
        """执行任务。"""
        pass

# 具体命令1：训练模型任务
class TrainModelCommand(Task):
    """
    一个具体的命令，封装了训练模型的请求。
    """
    def __init__(self, model_name, dataset_path):
        self._model_name = model_name
        self._dataset_path = dataset_path

    def execute(self):
        # 模拟执行训练任务
        print(f"正在训练模型: {self._model_name}，使用数据集: {self._dataset_path}")
        # 在这里可以调用具体的训练函数，如: train_model(self._model_name, self._dataset_path)

# 具体命令2：模型推理任务
class PredictCommand(Task):
    """
    一个具体的命令，封装了模型推理的请求。
    """
    def __init__(self, model_name, input_data):
        self._model_name = model_name
        self._input_data = input_data

    def execute(self):
        # 模拟执行推理任务
        print(f"正在使用模型: {self._model_name} 进行推理，输入数据: {self._input_data}")
        # 在这里可以调用具体的推理函数，如: predict(self._model_name, self._input_data)

# 请求者/调度器
class TaskScheduler:
    """
    一个请求者，它负责接收和执行命令。
    """
    def __init__(self):
        self._command_queue = []

    def add_command(self, command: Task):
        """将命令添加到队列中。"""
        self._command_queue.append(command)
        print(f"任务已添加到队列: {command.__class__.__name__}")

    def run_tasks(self):
        """按顺序执行队列中的所有任务。"""
        print("\n--- 正在执行所有任务 ---")
        while self._command_queue:
            command = self._command_queue.pop(0)
            command.execute()
        print("--- 所有任务执行完毕 ---")

# 客户端代码
scheduler = TaskScheduler()

# 客户端创建具体的命令对象，并将其添加到调度器中
train_command = TrainModelCommand(model_name="ResNet50", dataset_path="/data/cifar10")
predict_command = PredictCommand(model_name="ResNet50", input_data="image_001.jpg")

scheduler.add_command(train_command)
scheduler.add_command(predict_command)

# 调度器按顺序执行任务，客户端无需关心具体执行细节
scheduler.run_tasks()