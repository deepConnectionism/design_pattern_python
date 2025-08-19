import numpy as np
import torch
from abc import ABC, abstractmethod
# import tensorflow as tf

# 客户端期望的通用模型接口
class UniversalModel(ABC):
    @abstractmethod
    def predict(self, input_data):
        pass

# 被适配者1：一个 PyTorch 模型
class PyTorchModel:
    def predict_with_torch(self, input_tensor):
        print("PyTorch 模型正在进行推理...")
        return torch.tensor([0.9, 0.1])

# 适配器1：将 PyTorch 模型适配为通用接口
class PyTorchModelAdapter(UniversalModel):
    def __init__(self, model):
        self._model = model

    def predict(self, input_data):
        # 将输入数据适配为 PyTorch 张量
        input_tensor = torch.from_numpy(input_data)
        # 调用被适配者的特定方法
        output_tensor = self._model.predict_with_torch(input_tensor)
        # 将输出适配为 NumPy 数组
        return output_tensor.numpy()

# 被适配者2：一个 TensorFlow 模型
class TensorFlowModel:
    def run_inference(self, input_array):
        print("TensorFlow 模型正在进行推理...")
        return np.array([0.8, 0.2])

# 适配器2：将 TensorFlow 模型适配为通用接口
class TensorFlowModelAdapter(UniversalModel):
    def __init__(self, model):
        self._model = model

    def predict(self, input_data):
        # TensorFlow 和 NumPy 兼容，直接调用
        return self._model.run_inference(input_data)
        
# 客户端代码可以一致地使用任何一种模型
torch_model = PyTorchModelAdapter(PyTorchModel())
tf_model = TensorFlowModelAdapter(TensorFlowModel())

input_data = np.random.rand(1, 10)

print(f"PyTorch 模型的预测结果: {torch_model.predict(input_data)}")
print(f"TensorFlow 模型的预测结果: {tf_model.predict(input_data)}")