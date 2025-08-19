# 子系统1：数据处理
class DataHandler:
    def load_data(self, dataset_path):
        print(f"数据处理器：正在加载数据集从 {dataset_path}")
        # 模拟数据加载和预处理
        return "预处理好的数据"

# 子系统2：模型构建
class ModelBuilder:
    def build_model(self, model_type):
        print(f"模型构建器：正在构建 {model_type} 模型")
        # 模拟模型构建
        return "训练好的模型"

# 子系统3：模型评估
class Evaluator:
    def evaluate_model(self, model, data):
        print("评估器：正在评估模型性能...")
        # 模拟模型评估
        print("评估结果：准确率 95%")

# 门面类
class TrainingFacade:
    """
    门面类，为复杂的训练流水线提供一个简化的接口。
    """
    def __init__(self):
        # 门面类组合了所有的子系统
        self._data_handler = DataHandler()
        self._model_builder = ModelBuilder()
        self._evaluator = Evaluator()

    def train_model(self, model_type, dataset_path):
        """
        一个简化的、高层次的训练接口。
        """
        print(f"门面：接收到训练请求，模型类型: {model_type}, 数据集: {dataset_path}")
        
        # 门面负责协调和调用子系统中的复杂方法
        data = self._data_handler.load_data(dataset_path)
        model = self._model_builder.build_model(model_type)
        self._evaluator.evaluate_model(model, data)
        
        print("门面：训练流水线已完成。")

# 客户端代码
print("客户端：正在准备训练模型，通过门面进行操作...")
# 客户端只需要与门面类交互
facade = TrainingFacade()
facade.train_model(model_type="ResNet50", dataset_path="/data/cifar10")
print("客户端：操作已完成。")

print("\n--- 如果没有门面，客户端代码会更复杂 ---")
# 如果没有门面，客户端必须直接与所有子系统交互
data_handler = DataHandler()
model_builder = ModelBuilder()
evaluator = Evaluator()

raw_data = data_handler.load_data("/data/cifar10")
built_model = model_builder.build_model("ResNet50")
evaluator.evaluate_model(built_model, raw_data)