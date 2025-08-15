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