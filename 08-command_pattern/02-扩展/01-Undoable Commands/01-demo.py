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