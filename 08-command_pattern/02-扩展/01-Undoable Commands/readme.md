太棒了！可撤销的命令是命令模式最强大的应用之一。它能让你轻松地为程序添加“撤销”功能，这在许多算法和数据处理场景中都非常有用。

### 概略介绍解决方案

我们将通过一个具体的例子来学习**可撤销的命令**。我们的目标是构建一个简单的**超参数调整器**，它能对模型的学习率进行调整，并支持**撤销**和**重做**操作。

我们将使用命令模式来封装每一次学习率的调整操作。每个命令对象会记住调整前后的学习率，从而实现撤销和重做。一个**历史管理器**（`HistoryManager`）会负责存储这些命令，并提供撤销和重做的接口。

-----

### 代码和实现说明

我们的目标是创建一个可撤销的命令，并使用一个历史管理器来管理它。

#### 步骤 1: 定义核心组件

首先，我们定义一个模拟的模型类 `Model`，一个抽象的命令接口 `Command`，以及一个具体的命令类 `SetLearningRateCommand`。

```python
from abc import ABC, abstractmethod

# 模拟一个简单的模型，拥有一个可被修改的属性
class Model:
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

# 抽象命令接口，包含 execute 和 undo 方法
class Command(ABC):
    @abstractmethod
    def execute(self):
        """执行命令。"""
        pass

    @abstractmethod
    def undo(self):
        """撤销命令。"""
        pass

# 具体的可撤销命令
class SetLearningRateCommand(Command):
    def __init__(self, model: Model, new_lr: float):
        self._model = model
        self._new_lr = new_lr
        self._old_lr = model.learning_rate  # 存储旧状态，以便于撤销

    def execute(self):
        print(f"执行命令：学习率从 {self._old_lr} 调整为 {self._new_lr}")
        self._model.learning_rate = self._new_lr

    def undo(self):
        print(f"撤销命令：学习率从 {self._new_lr} 恢复为 {self._old_lr}")
        self._model.learning_rate = self._old_lr
```

**设计思路解释：**

  * **`Model`**: 这是命令的**接收者（Receiver）**，它执行实际的操作。
  * **`Command`**: 这是**命令接口**。每个可撤销的命令都必须实现 `execute` 和 `undo`。
  * **`SetLearningRateCommand`**: 这是具体的**命令**。它将 `Model` 对象和 `new_lr` 参数都封装在自身中，并在 `__init__` 中记录了操作前的状态（`_old_lr`）。

-----

#### 步骤 2: 编写历史管理器（请求者）

接下来，我们编写一个**历史管理器** `HistoryManager`。它负责存储已执行的命令，并提供撤销和重做的功能。

```python
class HistoryManager:
    """
    一个历史管理器，负责存储可撤销的命令，并提供撤销/重做功能。
    """
    def __init__(self):
        self._history = []  # 存储已执行的命令
        self._current_index = -1  # 指向当前可重做的最后一个命令

    def execute_command(self, command: Command):
        """执行命令，并将其添加到历史记录中。"""
        # 清除当前索引之后的所有重做历史
        if self._current_index < len(self._history) - 1:
            self._history = self._history[:self._current_index + 1]

        command.execute()
        self._history.append(command)
        self._current_index += 1

    def undo(self):
        """撤销最近的一个命令。"""
        if self._current_index >= 0:
            command_to_undo = self._history[self._current_index]
            command_to_undo.undo()
            self._current_index -= 1
        else:
            print("无法撤销：已是历史记录的起点。")

    def redo(self):
        """重做最近的一个已撤销的命令。"""
        if self._current_index < len(self._history) - 1:
            self._current_index += 1
            command_to_redo = self._history[self._current_index]
            command_to_redo.execute()
        else:
            print("无法重做：已是历史记录的终点。")
```

**设计思路解释：**

  * **`_history`**: 这是一个列表，用来存储执行过的所有命令。
  * **`_current_index`**: 这是关键。它是一个指针，指向当前的历史记录位置。`undo` 操作会使它后移，`redo` 操作会使它前移。
  * **`execute_command`**: 在执行新命令前，它会**清除重做历史**，这是一个典型的设计，因为执行新命令会覆盖之前的重做路径。

-----

#### 3\. 客户端代码（使用可撤销的命令）

现在，让我们来模拟一个超参数调整的场景，并使用我们的历史管理器。

```python
# 客户端代码
model = Model(learning_rate=0.01)
history_manager = HistoryManager()

print(f"初始学习率: {model.learning_rate}\n")

# 步骤 1：调整学习率到 0.001
command1 = SetLearningRateCommand(model, 0.001)
history_manager.execute_command(command1)
print(f"当前学习率: {model.learning_rate}\n")

# 步骤 2：再次调整学习率到 0.0001
command2 = SetLearningRateCommand(model, 0.0001)
history_manager.execute_command(command2)
print(f"当前学习率: {model.learning_rate}\n")

# 撤销最近一次操作
history_manager.undo()
print(f"撤销后学习率: {model.learning_rate}\n")

# 再次撤销
history_manager.undo()
print(f"再次撤销后学习率: {model.learning_rate}\n")

# 尝试再次撤销，将失败
history_manager.undo()

print("\n--- 尝试重做 ---")
# 重做上一次的撤销
history_manager.redo()
print(f"重做后学习率: {model.learning_rate}\n")

# 再次重做
history_manager.redo()
print(f"再次重做后学习率: {model.learning_rate}\n")

# 尝试再次重做，将失败
history_manager.redo()
```

**如何实现：**

1.  将上述所有代码块复制到你的 Python 文件中。
2.  运行代码，观察 `undo` 和 `redo` 操作如何改变模型的学习率。

**执行结果示例：**

```
初始学习率: 0.01

执行命令：学习率从 0.01 调整为 0.001
当前学习率: 0.001

执行命令：学习率从 0.001 调整为 0.0001
当前学习率: 0.0001

撤销命令：学习率从 0.0001 恢复为 0.001
撤销后学习率: 0.001

撤销命令：学习率从 0.001 恢复为 0.01
再次撤销后学习率: 0.01

无法撤销：已是历史记录的起点。

--- 尝试重做 ---
执行命令：学习率从 0.01 调整为 0.001
重做后学习率: 0.001

执行命令：学习率从 0.001 调整为 0.0001
再次重做后学习率: 0.0001

无法重做：已是历史记录的终点。
```

-----

### 总结

现在你已经掌握了**可撤销命令**的完整实现。通过将每个操作封装为独立的命令对象，我们实现了命令的**可逆**，并利用一个**历史管理器**来轻松地管理这些操作。