from abc import ABC, abstractmethod

# 定义特征工程的抽象基类
class FeatureProcessor(ABC):
    """特征处理器的抽象基类。"""
    @abstractmethod
    def process(self, data):
        """抽象方法：对数据进行处理。"""
        pass

# 标准化处理器
class StandardScaler(FeatureProcessor):
    """对数据进行标准化的具体实现。"""
    def process(self, data):
        print("正在使用 StandardScaler 对数据进行标准化...")
        return [((x - sum(data)/len(data)) / (max(data)-min(data))) for x in data] # 简化版实现

# 归一化处理器
class MinMaxScaler(FeatureProcessor):
    """对数据进行归一化的具体实现。"""
    def process(self, data):
        print("正在使用 MinMaxScaler 对数据进行归一化...")
        return [(x - min(data)) / (max(data) - min(data)) for x in data] # 简化版实现

class ProcessorFactory:
    """根据名称创建特征处理器的工厂类。"""
    @staticmethod
    def create_processor(processor_name):
        """
        工厂方法：根据传入的名称返回对应的处理器实例。
        如果名称无效，则抛出异常。
        """
        if processor_name == 'standard':
            return StandardScaler()
        elif processor_name == 'minmax':
            return MinMaxScaler()
        else:
            raise ValueError(f"未知处理器类型: {processor_name}")

# 客户端代码，完全不需要知道具体的处理器类名
data = [10, 20, 30, 40, 50]

# 使用工厂创建标准化处理器
try:
    standard_processor = ProcessorFactory.create_processor('standard')
    standardized_data = standard_processor.process(data)
    print(f"标准化后的数据: {standardized_data}")

    print("---")

    # 使用工厂创建归一化处理器
    minmax_processor = ProcessorFactory.create_processor('minmax')
    minmax_data = minmax_processor.process(data)
    print(f"归一化后的数据: {minmax_data}")
    
    print("---")

    # 尝试创建未知的处理器
    unknown_processor = ProcessorFactory.create_processor('invalid')
except ValueError as e:
    print(e)