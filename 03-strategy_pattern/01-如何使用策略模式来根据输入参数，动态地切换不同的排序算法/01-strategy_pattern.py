from abc import ABC, abstractmethod

# 定义排序策略的抽象基类
class SortingStrategy(ABC):
    """排序策略的抽象基类。"""
    @abstractmethod
    def sort(self, data):
        """抽象方法：对数据进行排序。"""
        pass

# 冒泡排序的具体策略
class BubbleSortStrategy(SortingStrategy):
    """冒泡排序算法的具体实现。"""
    def sort(self, data):
        print("使用冒泡排序...")
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

# 快速排序的具体策略
class QuickSortStrategy(SortingStrategy):
    """快速排序算法的具体实现。"""
    def sort(self, data):
        print("使用快速排序...")
        # 简化版实现，直接调用 Python 内置的排序函数作为演示
        return sorted(data)

class Sorter:
    """排序上下文类，它持有并使用一个排序策略。"""
    def __init__(self, strategy: SortingStrategy):
        # 构造函数中传入具体的策略对象
        self._strategy = strategy

    def set_strategy(self, strategy: SortingStrategy):
        # 允许在运行时切换策略
        self._strategy = strategy

    def sort_data(self, data):
        # 调用策略对象的 sort 方法来执行排序
        return self._strategy.sort(data)

# 客户端代码
data_to_sort = [64, 34, 25, 12, 22, 11, 90]

# 创建一个上下文，并传入冒泡排序策略
sorter = Sorter(BubbleSortStrategy())
sorted_data_bubble = sorter.sort_data(data_to_sort.copy()) # 使用 .copy() 以免修改原始列表
print(f"冒泡排序后的结果: {sorted_data_bubble}")

print("---")

# 在运行时切换策略，使用快速排序
sorter.set_strategy(QuickSortStrategy())
sorted_data_quick = sorter.sort_data(data_to_sort.copy())
print(f"快速排序后的结果: {sorted_data_quick}")