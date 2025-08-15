import time
import functools

def timer(func):
    """
    一个用于计算函数执行时间的装饰器。
    """
    # 使用 @functools.wraps 保持被装饰函数的元信息（如函数名、文档字符串）
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 记录函数开始执行的时间
        start_time = time.perf_counter()
        # 调用原始函数
        result = func(*args, **kwargs)
        # 记录函数结束执行的时间
        end_time = time.perf_counter()
        # 计算总耗时
        run_time = end_time - start_time
        print(f"函数 {func.__name__!r} 执行耗时: {run_time:.4f} 秒")
        # 返回原始函数的执行结果
        return result
    return wrapper


# 将 @timer 放在你想要计时的函数上方
@timer
def my_complex_calculation(n):
    """
    一个模拟复杂计算的函数。
    """
    time.sleep(n)
    return f"计算完成！模拟耗时 {n} 秒。"

@timer
def another_function(a, b):
    time.sleep(0.5)
    return a + b

# 调用被装饰的函数
print(my_complex_calculation(2))
print("---")
print(another_function(3, 5))