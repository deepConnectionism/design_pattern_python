from abc import ABC, abstractmethod

# 抽象模板类
class TrainingPipeline(ABC):
    """
    定义一个通用的训练算法骨架。
    """
    def run_pipeline(self, dataset):
        """
        这就是我们的模板方法。它定义了算法的骨架。
        """
        print("--- 正在运行训练流水线 ---")
        self.load_data(dataset)
        self.preprocess_data()
        self.train_model()
        self.evaluate_model()
        print("--- 训练流水线已完成 ---")

    @abstractmethod
    def load_data(self, dataset):
        """加载数据，由子类实现。"""
        pass

    @abstractmethod
    def preprocess_data(self):
        """数据预处理，由子类实现。"""
        pass
    
    @abstractmethod
    def train_model(self):
        """训练模型，由子类实现。"""
        pass
        
    def evaluate_model(self):
        """评估模型，默认实现，子类可以选择重写。"""
        print("评估模型：正在计算默认的准确率指标。")

# 具体子类1：图像分类器
class ImageClassifier(TrainingPipeline):
    def load_data(self, dataset):
        print(f"图像分类器：正在从 {dataset} 加载图像数据...")

    def preprocess_data(self):
        print("图像分类器：正在进行图像缩放和归一化...")

    def train_model(self):
        print("图像分类器：正在训练 ResNet 模型...")
        
    def evaluate_model(self):
        # 子类重写了评估方法
        print("图像分类器：正在计算准确率和 F1 分数...")

# 具体子类2：文本分类器
class TextClassifier(TrainingPipeline):
    def load_data(self, dataset):
        print(f"文本分类器：正在从 {dataset} 加载文本数据...")

    def preprocess_data(self):
        print("文本分类器：正在进行文本分词和词向量转换...")

    def train_model(self):
        print("文本分类器：正在训练 BERT 模型...")
        
    # 子类使用父类的默认评估方法
    # def evaluate_model(self):
    #     super().evaluate_model()

# 客户端代码
print("--- 运行图像分类训练流程 ---")
image_classifier = ImageClassifier()
# 客户端只调用模板方法，无需关心内部细节
image_classifier.run_pipeline("ImageNet")

print("\n--- 运行文本分类训练流程 ---")
text_classifier = TextClassifier()
# 客户端使用相同的方法，但执行了不同的流程细节
text_classifier.run_pipeline("SQuAD")