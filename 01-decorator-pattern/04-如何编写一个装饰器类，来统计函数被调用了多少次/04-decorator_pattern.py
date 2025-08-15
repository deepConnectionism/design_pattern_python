import functools

class CallCounter:
    """
    一个用于统计函数调用次数的装饰器类。
    """
    def __init__(self, func):
        # 这是装饰器的第一步：在实例化时接收被装饰的函数
        self.func = func
        # 将被装饰函数的元信息复制到装饰器实例上
        functools.update_wrapper(self, func)
        # 维护状态：初始化调用次数为 0
        self.calls = 0

    def __call__(self, *args, **kwargs):
        # 这是装饰器的第二步：当装饰器实例被调用时，执行此方法
        # 增加调用次数
        self.calls += 1
        print(f"函数 {self.func.__name__!r} 被调用了 {self.calls} 次")
        # 调用原始函数并返回结果
        return self.func(*args, **kwargs)

# 将 @CallCounter 放在你想要统计调用次数的函数上方
@CallCounter
def add_numbers(a, b):
    """
    一个简单的加法函数。
    """
    return a + b

@CallCounter
def say_hello():
    """
    一个简单的问候函数。
    """
    return "Hello!"

# 调用被装饰的函数
print(f"结果: {add_numbers(3, 5)}")
print(f"结果: {add_numbers(10, 20)}")
print("---")
print(f"结果: {say_hello()}")
print(f"结果: {say_hello()}")
print(f"结果: {say_hello()}")

# 你还可以直接访问装饰器实例的属性，查看调用次数
print(f"add_numbers 函数总共被调用了 {add_numbers.calls} 次。")