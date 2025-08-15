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

# 具体主题：训练监控器
class TrainingMonitor(Subject):
    def __init__(self):
        # 存储所有注册的观察者
        self._observers = []
        self._status = None  # 训练状态

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        # 状态改变时，通知所有观察者
        self.notify()

    def attach(self, observer: Observer):
        print(f"观察者 {observer.__class__.__name__} 已注册。")
        self._observers.append(observer)

    def detach(self, observer: Observer):
        print(f"观察者 {observer.__class__.__name__} 已移除。")
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def run_training_step(self, epoch):
        print(f"\n--- Epoch {epoch} 训练中 ---")
        # 模拟训练步骤
        import random
        acc = random.uniform(0.5, 0.95)
        self.status = {"epoch": epoch, "accuracy": acc}
        
# 具体观察者1：日志记录器
class Logger(Observer):
    def update(self, subject: Subject):
        if subject.status:
            print(f"Logger: Epoch {subject.status['epoch']} 的准确率为 {subject.status['accuracy']:.2f}")

# 具体观察者2：早停器
class EarlyStopper(Observer):
    def update(self, subject: Subject):
        if subject.status and subject.status['accuracy'] > 0.90:
            print(f"EarlyStopper: 准确率 {subject.status['accuracy']:.2f} 已超过阈值，准备停止训练。")

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
    # 如果早停条件触发，可以移除观察者或直接中断
    if monitor.status and monitor.status['accuracy'] > 0.90:
        print("--- 训练提前终止 ---")
        break

# 移除观察者
print("\n训练结束，移除 EarlyStopper")
monitor.detach(stopper)