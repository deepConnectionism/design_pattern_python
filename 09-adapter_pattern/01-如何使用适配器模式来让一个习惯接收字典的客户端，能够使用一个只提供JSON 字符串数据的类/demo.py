import json

# 客户端期望的接口
class DataProcessor:
    def process_data(self, data: dict):
        """
        这个处理器只接受字典格式的数据。
        """
        print("正在处理字典格式的数据...")
        print(f"数据类型: {type(data)}, 键: {list(data.keys())}")
        # 这里是实际的数据处理逻辑

# 需要被适配的类，它返回 JSON 字符串
class LegacyDataFetcher:
    def get_data(self):
        """
        返回一个 JSON 格式的字符串，而不是字典。
        """
        print("正在获取 JSON 格式的原始数据...")
        return '{"feature1": 100, "feature2": 200, "label": "A"}'
    
    
# 适配器类
class JsonDataAdapter:
    """
    适配器，将 LegacyDataFetcher 的接口适配为客户端期望的接口。
    """
    def __init__(self, adaptee: LegacyDataFetcher):
        self._adaptee = adaptee

    def get_compatible_data(self):
        """
        将 JSON 字符串转换为字典，从而适配客户端。
        """
        # 从被适配者那里获取不兼容的原始数据
        json_data = self._adaptee.get_data()
        
        # 核心逻辑：进行数据转换
        dict_data = json.loads(json_data)
        
        # 返回适配后的数据
        print("适配器：已将 JSON 字符串转换为字典。")
        return dict_data
    
# 客户端代码
processor = DataProcessor()
data_fetcher = LegacyDataFetcher()

# 创建适配器，将数据获取器适配到客户端的期望
adapter = JsonDataAdapter(data_fetcher)

# 客户端通过适配器获取兼容的数据，然后进行处理
print("客户端：正在通过适配器获取数据...")
compatible_data = adapter.get_compatible_data()
print("客户端：已获取兼容数据，准备处理...")
processor.process_data(compatible_data)

print("\n---")
# 如果没有适配器，客户端将无法直接处理原始数据
try:
    processor.process_data(data_fetcher.get_data())
except TypeError as e:
    print(f"错误：无法直接处理不兼容的数据。类型错误: {e}")