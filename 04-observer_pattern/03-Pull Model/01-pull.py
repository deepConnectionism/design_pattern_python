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