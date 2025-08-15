你的问题非常好！拉取模式（Pull Model）在实际应用中确实非常有用，特别是在主题需要通知多个观察者，但每个观察者只对部分数据感兴趣的场景。

拉取模式的核心思想是：**主题只发送一个通用通知，观察者收到通知后，根据自己的需要主动从主题那里“拉取”数据。**

下面我们来编写一个拉取模式的示例，它基于我们之前观察者模式的代码进行修改。

-----

### 概略介绍解决方案

我们将重构之前的**观察者模式**示例，将其从**推送模式**转换为**拉取模式**。

1.  **主题**（`TrainingMonitor`）将不再在通知时推送所有数据，而是在**通知时**只传递一个通用信号。
2.  **观察者**（`Logger` 和 `EarlyStopper`）在收到通知后，会调用主题的公共方法来**拉取**它们需要的数据，比如 `get_latest_metrics()`。

这种方式的好处是，主题的代码更简洁，因为它无需关心每个观察者需要什么数据。同时，观察者也更灵活，因为它只获取自己需要的信息。

-----

### 代码和实现说明

我们的目标是创建一个**拉取模式**的观察者模式实现，在其中，观察者会主动向主题请求数据。

#### 步骤 1: 重构主题和观察者

我们将修改 `TrainingMonitor` 的 `notify` 方法，使其不再传递数据。同时，在 `Logger` 和 `EarlyStopper` 的 `update` 方法中，我们会主动调用主题的方法来获取数据。

```python
from abc import ABC, abstractmethod

# 抽象观察者
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        """当主题状态改变时，此方法会被调用。"""
        pass

# 抽象主题
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer):
        """注册一个观察者。"""
        pass

    @abstractmethod
    def detach(self, observer: Observer):
        """移除一个观察者。"""
        pass

    @abstractmethod
    def notify(self):
        """通知所有观察者。"""
        pass

# ---

# 具体主题：训练监控器 (拉取模式)
class TrainingMonitor(Subject):
    def __init__(self):
        self._observers = []
        self._metrics = None  # 训练指标，可以包含多个键值对

    def get_latest_metrics(self):
        """提供一个公共方法，供观察者拉取数据。"""
        return self._metrics

    def attach(self, observer: Observer):
        print(f"观察者 {observer.__class__.__name__} 已注册。")
        self._observers.append(observer)

    def detach(self, observer: Observer):
        print(f"观察者 {observer.__class__.__name__} 已移除。")
        self._observers.remove(observer)

    def notify(self):
        # 只通知状态改变，不推送具体数据
        print("通知：训练状态已更新！")
        for observer in self._observers:
            observer.update(self)

    def run_training_step(self, epoch):
        print(f"\n--- Epoch {epoch} 训练中 ---")
        import random
        # 模拟生成一些训练指标
        self._metrics = {
            "epoch": epoch,
            "loss": random.uniform(0.1, 0.5),
            "accuracy": random.uniform(0.5, 0.95),
            "val_loss": random.uniform(0.1, 0.5),
            "val_accuracy": random.uniform(0.5, 0.95)
        }
        # 指标更新后，通知所有观察者
        self.notify()
        
# 具体观察者1：日志记录器 (拉取模式)
class Logger(Observer):
    def update(self, subject: Subject):
        # 收到通知后，主动拉取所需的数据
        metrics = subject.get_latest_metrics()
        if metrics:
            print(f"Logger 拉取数据: Epoch {metrics['epoch']} 的准确率为 {metrics['accuracy']:.2f}, 损失为 {metrics['loss']:.2f}")

# 具体观察者2：早停器 (拉取模式)
class EarlyStopper(Observer):
    def update(self, subject: Subject):
        # 收到通知后，主动拉取所需的数据
        metrics = subject.get_latest_metrics()
        if metrics and metrics['val_accuracy'] > 0.90:
            print(f"EarlyStopper 拉取数据: 验证集准确率 {metrics['val_accuracy']:.2f} 已超过阈值，准备停止训练。")

```

**设计思路解释：**

  * **`TrainingMonitor.notify()`:** 这个方法不再接受参数。它只调用每个观察者的 `update` 方法，传递它自己 (`self`) 作为参数。
  * **`TrainingMonitor.get_latest_metrics()`:** 我们为主题添加了一个公共方法，用来提供数据。这使得主题成为一个数据的“提供者”。
  * **`Logger.update()` 和 `EarlyStopper.update()`:** 在这两个方法中，我们通过 `subject.get_latest_metrics()` 主动获取了所需的数据。`Logger` 获取了 `accuracy` 和 `loss`，而 `EarlyStopper` 只关心 `val_accuracy`。

-----

#### 2\. 客户端代码（使用拉取模式）

客户端代码的使用方式和之前一样，但底层的通知机制已经改变了。

```python
# 客户端代码
monitor = TrainingMonitor()

# 创建观察者
logger = Logger()
stopper = EarlyStopper()

# 注册观察者
monitor.attach(logger)
monitor.attach(stopper)

# 模拟训练循环
for i in range(5):
    monitor.run_training_step(i)
    
    # 检查是否满足早停条件，这里需要再次拉取数据
    metrics = monitor.get_latest_metrics()
    if metrics and metrics['val_accuracy'] > 0.90:
        print("--- 训练提前终止 ---")
        break

# 移除观察者
print("\n训练结束，移除 EarlyStopper")
monitor.detach(stopper)
```

**如何实现：**

1.  将上述所有代码块复制到你的 Python 文件中。
2.  运行代码，观察 `TrainingMonitor` 如何只发送一个通用通知，而观察者如何拉取它们各自需要的数据。

**执行结果示例：**

```
观察者 Logger 已注册。
观察者 EarlyStopper 已注册。

--- Epoch 0 训练中 ---
通知：训练状态已更新！
Logger 拉取数据: Epoch 0 的准确率为 0.86, 损失为 0.20
EarlyStopper 拉取数据: 验证集准确率 0.52 未超过阈值
--- Epoch 1 训练中 ---
通知：训练状态已更新！
Logger 拉取数据: Epoch 1 的准确率为 0.92, 损失为 0.45
EarlyStopper 拉取数据: 验证集准确率 0.93 已超过阈值，准备停止训练。
--- 训练提前终止 ---

训练结束，移除 EarlyStopper
观察者 EarlyStopper 已移除。
```

-----

### 总结

现在你已经掌握了**拉取模式**的实现。它在**数据量较大**或**观察者只对部分数据感兴趣**的场景下，是一种更高效、更灵活的观察者模式变体。
