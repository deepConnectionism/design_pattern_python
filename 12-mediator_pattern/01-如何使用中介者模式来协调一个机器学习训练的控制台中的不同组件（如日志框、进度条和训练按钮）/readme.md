感谢你整理了已经学习过的设计模式！这太棒了。你已经掌握了以下模式：

  * **创建型模式**：工厂模式
  * **结构型模式**：装饰器模式、代理模式、组合模式、适配器模式、门面模式
  * **行为型模式**：观察者模式、策略模式、迭代器模式、命令模式、模板方法模式

你已经对面向对象设计有了非常坚实的基础。接下来，我们继续学习一个新的行为型模式：**中介者模式 (Mediator Pattern)**。

-----

### 概略介绍解决方案

**中介者模式**是一种**行为型模式**，它的核心思想是：用一个**中介者对象**来封装一系列对象之间的交互。中介者使得各对象不需要显式地相互引用，从而实现了松散耦合，并且可以独立地改变它们之间的交互。

简单来说，中介者模式就像一个**交通管制员**。它负责协调十字路口的所有车辆，告诉它们何时前进，何时停车。如果没有这个管制员，每辆车都需要和其他所有车辆直接通信，这会让情况变得混乱不堪。

在你的算法和机器学习项目中，这个模式的应用场景非常广泛，例如：

  * **复杂系统通信**：当一个系统由多个独立组件组成时（如数据加载器、模型、评估器和日志记录器），它们之间的交互可能会非常复杂。中介者可以作为中央协调者，处理所有通信。
  * **参数同步**：在分布式机器学习中，你可能有多个工作节点，它们需要将梯度或参数更新同步到参数服务器。中介者可以处理这些节点之间的通信和同步逻辑。
  * **GUI（图形用户界面）**：如果你在构建一个带有界面的数据分析工具，不同的 UI 组件（如按钮、文本框、图表）需要相互通信。中介者可以协调这些组件的交互。

如果没有中介者模式，各个对象之间会形成复杂的网状连接，导致代码难以理解和维护。中介者模式通过引入一个中央协调者，将复杂的网状交互转化为简单的星形交互。

我们将通过一个具体的例子来学习：如何使用中介者模式来协调一个**机器学习训练的控制台**中的不同组件（如日志框、进度条和训练按钮）。

-----

### 代码和实现说明

我们的目标是创建一个**中介者接口** `Mediator`，然后实现一个具体的**中介者类** `TrainingMediator`。同时，我们还将定义**同事类** `LogDisplay`、`ProgressBar` 和 `TrainButton`，它们通过中介者进行交互。

#### 步骤 1: 定义中介者接口和抽象同事类

首先，我们定义一个中介者接口 `Mediator`，以及一个抽象的**同事类** `Component`。

```python
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
```

**设计思路解释：**

  * **`Mediator`**：这是我们的中介者接口，它定义了 `notify` 方法。所有组件都会通过这个方法向中介者发送通知。
  * **`Component`**：这是抽象的同事类。它持有中介者的引用，并能通过 `set_mediator` 方法设置中介者。所有具体的组件都将继承它。

-----

#### 步骤 2: 编写具体同事类

接下来，我们编写具体的同事类，它们负责各自的功能，并通过中介者进行通信。

```python
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
```

**设计思路解释：**

  * **`TrainButton`**：当按钮被点击时，它不直接操作日志或进度条，而是通过中介者发送一个 `train_clicked` 事件。
  * **`LogDisplay` 和 `ProgressBar`**：它们有自己的功能方法，但不会主动发起通信。它们只响应来自中介者的命令。

-----

#### 3\. 编写具体中介者类

现在，我们编写**中介者类** `TrainingMediator`。它是模式的核心，负责协调所有组件之间的交互逻辑。

```python
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

```

**设计思路解释：**

  * **`TrainingMediator`**：这个类组合了所有需要协调的组件。
  * **`notify()`**：这是中介者的核心方法。它根据**发送者**和**事件类型**来决定如何协调其他组件。`TrainButton` 被点击后，它会通知中介者，中介者再反过来通知 `LogDisplay` 和 `ProgressBar`。
  * **`_do_training_simulation()`**：这是一个模拟训练过程的私有方法。它每完成一个步骤，就通知中介者。中介者再根据这个通知更新进度条和日志。

-----

#### 4\. 客户端代码（使用中介者模式）

现在，让我们看看客户端代码如何使用这个模式，以及它带来的好处。

```python
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
```

**如何实现：**

1.  将上述所有代码块复制到你的 Python 文件中。
2.  运行代码，观察 `TrainButton` 如何通过中介者间接地影响 `LogDisplay` 和 `ProgressBar`。

**执行结果示例：**

```
--- 正在初始化 UI 组件 ---
--- 正在创建中介者 ---

--- 客户端模拟点击训练按钮 ---
TrainButton: 被点击。
LogDisplay: 训练已启动。
ProgressBar: 进度更新到 0%
--- 模拟训练步骤 0.0 ---
ProgressBar: 进度更新到 0%
LogDisplay: 训练步骤 0.0 完成。
--- 模拟训练步骤 1.0 ---
ProgressBar: 进度更新到 20%
LogDisplay: 训练步骤 1.0 完成。
--- 模拟训练步骤 2.0 ---
ProgressBar: 进度更新到 40%
LogDisplay: 训练步骤 2.0 完成。
...
```

-----

### 总结

现在你已经掌握了**中介者模式**的实现。它通过引入一个中介者对象，将复杂的**网状连接**转化为简单的**星形连接**，从而实现了组件之间的**松散耦合**。这在你的算法项目中非常有用，能让你轻松地管理和扩展复杂的系统。
