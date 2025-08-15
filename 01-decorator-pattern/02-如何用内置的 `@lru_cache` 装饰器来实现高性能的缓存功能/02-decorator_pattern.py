import time
import functools

# 这是我们之前写的计时装饰器
def timer(func):
    """
    一个用于计算函数执行时间的装饰器。
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"函数 {func.__name__!r} 执行耗时: {run_time:.4f} 秒")
        return result
    return wrapper

# 斐波那契数列函数，计算量巨大，非常适合用来测试缓存效果
@timer
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 使用缓存装饰器来优化斐波那契函数
@timer
@functools.lru_cache(maxsize=None)
def fibonacci_with_cache(n):
    if n < 2:
        return n
    return fibonacci_with_cache(n-1) + fibonacci_with_cache(n-2)

print("---")
print("测试未缓存的斐波那契函数:")
result_uncached = fibonacci(30)
print(f"结果: {result_uncached}")

print("---")
print("测试已缓存的斐波那契函数:")
result_cached = fibonacci_with_cache(30)
print(f"结果: {result_cached}")
print("再次调用相同参数，这次应该会很快:")
result_cached_again = fibonacci_with_cache(30)
print(f"结果: {result_cached_again}")