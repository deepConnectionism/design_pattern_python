from abc import ABC, abstractmethod

# 抽象中介者接口
class Mediator(ABC):
    @abstractmethod
    def notify(self, sender, event):
        """处理来自组件的通知。"""
        pass

# 抽象同事类
class Component(ABC):
    def __init__(self, mediator: Mediator = None):
        self._mediator = mediator

    def set_mediator(self, mediator: Mediator):
        self._mediator = mediator

# 具体同事类1：训练按钮
class TrainButton(Component):
    def click(self):
        print("TrainButton: 被点击。")
        self._mediator.notify(self, "train_clicked")

# 具体同事类2：日志显示器
class LogDisplay(Component):
    def display_message(self, message):
        print(f"LogDisplay: {message}")

# 具体同事类3：进度条
class ProgressBar(Component):
    def update_progress(self, progress):
        print(f"ProgressBar: 进度更新到 {progress}%")

# 具体中介者类
class TrainingMediator(Mediator):
    def __init__(self, button, log_display, progress_bar):
        self._button = button
        self._log_display = log_display
        self._progress_bar = progress_bar

        # 设置每个组件的中介者引用
        self._button.set_mediator(self)
        self._log_display.set_mediator(self)
        self._progress_bar.set_mediator(self)

    def notify(self, sender, event):
        if sender == self._button and event == "train_clicked":
            self._log_display.display_message("训练已启动。")
            self._progress_bar.update_progress(0)
            self._do_training_simulation()
        elif event == "training_step_completed":
            progress = sender
            self._progress_bar.update_progress(progress)
            self._log_display.display_message(f"训练步骤 {progress/20} 完成。")
            if progress >= 100:
                self._log_display.display_message("训练完成。")

    def _do_training_simulation(self):
        # 模拟训练过程，并通知中介者
        for step in range(0, 101, 20):
            print(f"--- 模拟训练步骤 {step/20} ---")
            self.notify(step, "training_step_completed")

# 客户端代码
print("--- 正在初始化 UI 组件 ---")
train_button = TrainButton()
log_display = LogDisplay()
progress_bar = ProgressBar()

print("--- 正在创建中介者 ---")
# 客户端创建中介者，并将组件传递给它
mediator = TrainingMediator(train_button, log_display, progress_bar)

print("\n--- 客户端模拟点击训练按钮 ---")
train_button.click()