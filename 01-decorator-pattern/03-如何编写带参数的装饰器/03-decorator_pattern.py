import time
import functools

def timer_with_precision(precision=4):
    """
    一个带参数的计时装饰器，可以自定义打印精度。
    """
    # 这是装饰器的第一层：接收装饰器的参数
    def decorator(func):
        # 这是装饰器的第二层：接收被装饰的函数
        @functools.wraps(func)
        # 这是装饰器的第三层：执行实际的逻辑
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            print(f"函数 {func.__name__!r} 执行耗时: {run_time:.{precision}f} 秒")
            return result
        return wrapper
    return decorator

# 引入我们之前写的斐波那契函数
def fibonacci_complex(n):
    if n < 2:
        return n
    return fibonacci_complex(n-1) + fibonacci_complex(n-2)

# 使用带参数的装饰器，并传入 precision=6
@timer_with_precision(precision=6)
def my_complex_calculation_6_precision(n):
    """
    一个需要高精度计时的复杂计算函数。
    """
    fibonacci_complex(n)
    return "计算完成！"

# 使用带参数的装饰器，并使用默认的 precision=4
@timer_with_precision()
def my_complex_calculation_default_precision(n):
    """
    一个使用默认精度的复杂计算函数。
    """
    fibonacci_complex(n)
    return "计算完成！"

print("---")
print("测试高精度计时:")
print(my_complex_calculation_6_precision(30))

print("---")
print("测试默认精度计时:")
print(my_complex_calculation_default_precision(30))