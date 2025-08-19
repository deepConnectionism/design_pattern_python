from abc import ABC, abstractmethod

# 抽象组件接口
class Layer(ABC):
    """
    所有组件（无论是单个层还是组合模型）都必须实现的接口。
    """
    @abstractmethod
    def get_parameter_count(self):
        """返回该层或模型中的总参数数量。"""
        pass

# 叶子节点：一个具体的神经网络层
class DenseLayer(Layer):
    """
    一个具体的、无法再分解的层。
    """
    def __init__(self, neurons):
        self._neurons = neurons
        # 模拟计算参数量
        self._parameters = neurons * (neurons + 1)
        print(f"创建了一个 DenseLayer，参数量: {self._parameters}")

    def get_parameter_count(self):
        return self._parameters
    
# 组合对象：一个可以包含其他层的模型
class SequentialModel(Layer):
    """
    一个可以包含其他 Layer 对象的组合模型。
    """
    def __init__(self):
        self._layers = []

    def add_layer(self, layer: Layer):
        """向模型中添加一个 Layer 对象。"""
        self._layers.append(layer)

    def get_parameter_count(self):
        total_params = 0
        # 递归地遍历所有子层，并累加它们的参数量
        for layer in self._layers:
            total_params += layer.get_parameter_count()
        return total_params
    
# 客户端代码
print("--- 正在构建模型 ---")
# 创建一个复杂的组合模型
main_model = SequentialModel()

# 添加一个简单的 DenseLayer
layer1 = DenseLayer(neurons=10)
main_model.add_layer(layer1)

# 创建一个嵌套的子模型
sub_model = SequentialModel()
layer2 = DenseLayer(neurons=20)
layer3 = DenseLayer(neurons=30)
sub_model.add_layer(layer2)
sub_model.add_layer(layer3)

# 将子模型添加到主模型中
main_model.add_layer(sub_model)

# 客户端可以一致地处理单个层和组合模型
print("\n--- 计算参数量 ---")
# 客户端只调用 get_parameter_count()，无需关心它是单个层还是组合模型
total_params = main_model.get_parameter_count()
print(f"主模型的总参数量为: {total_params}")

# 也可以直接获取子模型的参数量
sub_model_params = sub_model.get_parameter_count()
print(f"子模型的总参数量为: {sub_model_params}")