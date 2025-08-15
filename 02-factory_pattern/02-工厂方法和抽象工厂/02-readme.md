你问到了一个关键点！我们之前学习的是**简单工厂模式**（Simple Factory Pattern），它是工厂模式最基础的一种形式，也是最常用的。

除了简单工厂，还有两种更复杂的工厂模式，它们在解决更复杂的问题时非常有用。了解这些，能让你在面对不同设计场景时做出更好的选择。

### 1\. 工厂方法模式 (Factory Method Pattern)

工厂方法模式的核心思想是：定义一个用于创建对象的接口，但让**子类**决定实例化哪一个类。这使得对象的创建过程延迟到子类。

**简单工厂 vs. 工厂方法**

| 特性 | 简单工厂 | 工厂方法 |
| :--- | :--- | :--- |
| 创建逻辑 | 集中在一个工厂类中 | 分散在多个子工厂类中 |
| 扩展性 | 违反开闭原则，每增加一个新产品就需要修改工厂类 | 符合开闭原则，增加新产品时只需添加新的工厂和产品类 |
| 复杂度 | 简单，但扩展性差 | 相对复杂，但扩展性强 |

**工厂方法模式的应用场景：**
当你需要一个**可扩展**的、能够轻松添加新对象的框架时，工厂方法模式是理想选择。

**代码示例：**

我们来重构之前的特征工程例子，用工厂方法模式来实现。

```python
from abc import ABC, abstractmethod

# 抽象产品：特征处理器
class FeatureProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass

# 具体产品：标准化处理器
class StandardScaler(FeatureProcessor):
    def process(self, data):
        print("正在使用 StandardScaler 对数据进行标准化...")
        return data

# 具体产品：归一化处理器
class MinMaxScaler(FeatureProcessor):
    def process(self, data):
        print("正在使用 MinMaxScaler 对数据进行归一化...")
        return data

# ---

# 抽象工厂：定义一个创建产品的接口
class ProcessorFactory(ABC):
    @abstractmethod
    def create_processor(self):
        pass

# 具体工厂：创建标准化处理器
class StandardScalerFactory(ProcessorFactory):
    def create_processor(self):
        return StandardScaler()

# 具体工厂：创建归一化处理器
class MinMaxScalerFactory(ProcessorFactory):
    def create_processor(self):
        return MinMaxScaler()

# ---

# 客户端代码
data = [1, 2, 3]

# 创建标准化工厂，然后通过工厂创建产品
standard_factory = StandardScalerFactory()
standard_processor = standard_factory.create_processor()
standard_processor.process(data)

# 创建归一化工厂，然后通过工厂创建产品
minmax_factory = MinMaxScalerFactory()
minmax_processor = minmax_factory.create_processor()
minmax_processor.process(data)
```

**设计思路解释：**

  * 我们不再有一个集中式的 `ProcessorFactory`，而是为每一种具体的处理器（`StandardScaler` 和 `MinMaxScaler`）创建了一个**独立的工厂**（`StandardScalerFactory` 和 `MinMaxScalerFactory`）。
  * 如果将来要添加新的处理器，比如 `RobustScaler`，我们只需要创建 `RobustScaler` 类和 `RobustScalerFactory` 类，而**无需修改**任何现有的代码。这就是它符合**开闭原则**的体现。

-----

### 2\. 抽象工厂模式 (Abstract Factory Pattern)

抽象工厂模式是工厂方法模式的升级版，它提供一个接口，用于创建**一系列相关或相互依赖的对象家族**，而无需指定它们具体的类。

**抽象工厂模式的应用场景：**
假设你的机器学习项目需要支持多种主题或配置（比如，"生产环境"和"开发环境"）。每种环境都需要创建一套完整的对象，比如数据加载器、模型和评估器。抽象工厂模式可以为你提供一个统一的接口来创建这些**整套**的对象。

**总结**

  * **简单工厂**：一个工厂，根据参数创建不同的对象。适用于对象种类较少且不常变动的情况。
  * **工厂方法**：一个抽象工厂，每个具体对象都有一个对应的具体工厂。适用于需要频繁添加新对象的场景。
  * **抽象工厂**：一个抽象工厂，每个具体工厂可以创建**一整套**相关联的对象。适用于需要支持多种“产品族”的复杂系统。

在你的日常算法项目中，**简单工厂模式**已经足够应对大多数情况，因为它简单直观。但如果你的项目需要高度的扩展性和灵活性，那么**工厂方法模式**会是更好的选择。

你对这两种更复杂的工厂模式还有疑问吗？如果没有，我们可以继续学习下一个设计模式：**策略模式**。