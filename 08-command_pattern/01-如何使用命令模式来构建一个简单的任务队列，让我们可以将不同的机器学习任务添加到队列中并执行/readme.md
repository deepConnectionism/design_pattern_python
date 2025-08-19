好的，我们继续！接下来，我们来学习一个在许多系统架构中都非常实用的设计模式：**命令模式 (Command Pattern)**。

### 概略介绍解决方案

**命令模式**是一种**行为型模式**，它的核心思想是：将一个请求封装为一个**命令对象**，从而使你能够用不同的请求对客户进行参数化，对请求进行排队或记录日志，并支持可撤销的操作。

简单来说，命令模式就是把**一个动作或请求**封装成一个对象。这个对象包含了执行该动作所需的所有信息，比如**执行者**（接收者）和**参数**。

在你的算法和机器学习项目中，这个模式的应用场景非常广泛，例如：

  * **任务调度和排队：** 你可以将不同的训练、推理或数据预处理任务封装为命令对象，然后放入一个队列中，由一个调度器按顺序或并发地执行。
  * **可撤销的操作：** 如果你的程序需要支持“撤销”功能，你可以将每个操作封装为命令对象，并将其记录在一个历史列表中。要撤销时，只需调用命令对象的 `undo` 方法。
  * **记录日志和事务：** 你可以将一系列操作封装为命令，然后记录到日志文件中，以便于重放或恢复。

如果没有命令模式，你可能会直接调用对象的各种方法，这使得你的代码与具体的执行者紧密耦合，难以实现上述功能。命令模式通过引入一个**命令对象**作为中间层，实现了**请求者**、**命令**和**执行者**之间的解耦。

我们将通过一个具体的例子来学习：如何使用命令模式来构建一个简单的**任务队列**，让我们可以将不同的机器学习任务添加到队列中并执行。

-----

### 代码和实现说明

我们的目标是创建一个**命令接口** `Task`，然后实现两个具体的命令 `TrainModelCommand` 和 `PredictCommand`，最后创建一个**请求者** `TaskScheduler` 来执行这些命令。

#### 步骤 1: 定义命令接口和具体命令

首先，我们定义一个命令接口 `Task`，并实现**具体命令** `TrainModelCommand` 和 `PredictCommand`。

```python
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
```

**设计思路解释：**

  * **`Task(ABC)`:** 这是我们的**命令接口**，它定义了 `execute` 方法，所有命令都必须实现它。
  * **`TrainModelCommand` 和 `PredictCommand`:** 这些是**具体命令**，它们封装了特定的动作。它们将执行者和参数（比如 `model_name`）都包含在自身中，使得 `execute` 方法可以独立执行。

-----

#### 步骤 2: 编写请求者（Invoker）

接下来，我们编写**请求者** `TaskScheduler`。它负责接收命令，并按照某种方式执行它们。

```python
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
```

**设计思路解释：**

  * **`TaskScheduler`:** 这是我们的**请求者**。它持有命令对象，但它**不关心**这些命令具体做什么。它只知道每个命令都有一个 `execute` 方法。
  * **`add_command()`:** 这个方法将命令对象添加到队列中，实现了**任务的排队**。
  * **`run_tasks()`:** 这个方法按顺序执行队列中的所有命令。

-----

#### 3\. 客户端代码（使用命令模式）

现在，让我们看看客户端代码如何使用这个模式，以及它带来的好处。

```python
# 客户端代码
scheduler = TaskScheduler()

# 客户端创建具体的命令对象，并将其添加到调度器中
train_command = TrainModelCommand(model_name="ResNet50", dataset_path="/data/cifar10")
predict_command = PredictCommand(model_name="ResNet50", input_data="image_001.jpg")

scheduler.add_command(train_command)
scheduler.add_command(predict_command)

# 调度器按顺序执行任务，客户端无需关心具体执行细节
scheduler.run_tasks()
```

**如何实现：**

1.  将上述所有代码块复制到你的 Python 文件中。
2.  运行代码，观察 `TaskScheduler` 如何按顺序执行两个不同的命令，而无需知道命令的内部实现。

**执行结果示例：**

```
任务已添加到队列: TrainModelCommand
任务已添加到队列: PredictCommand

--- 正在执行所有任务 ---
正在训练模型: ResNet50，使用数据集: /data/cifar10
正在使用模型: ResNet50 进行推理，输入数据: image_001.jpg
--- 所有任务执行完毕 ---
```

-----

### 总结

现在你已经掌握了**命令模式**的实现。它将请求、请求的执行者和请求的参数封装到一个对象中，从而实现了**请求者**和**执行者**的解耦。这使得你可以轻松地对请求进行排队、记录和撤销等操作。

在你的算法项目中，这种模式能帮助你构建一个灵活的任务调度系统，让你轻松管理各种训练和推理任务。