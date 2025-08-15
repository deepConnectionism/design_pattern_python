好的，我们继续深入学习装饰器！既然你已经掌握了如何用装饰器来计时，那我们来学习另一个在算法和机器学习项目中非常实用的应用：**缓存 (Caching)**。

### 概略介绍解决方案

很多算法和数据处理函数都有一个共同特点：当输入不变时，它们的输出也始终不变。对于这些计算量大、耗时长的函数，如果每次调用时都重新计算，会严重影响程序的性能。

**缓存装饰器**就能解决这个问题。它的核心思想是：

1.  在函数第一次被调用时，将**输入参数**和**计算结果**存储起来。
2.  下次再用同样的输入参数调用函数时，直接从存储中返回之前的结果，而不再重新执行函数体。

这能极大地提升性能，尤其是在需要重复调用相同函数的场景下。

我们将通过一个具体的例子来学习：如何创建一个缓存装饰器，来优化一个耗时的斐波那契数列计算函数。

-----

### 代码和实现说明

我们的目标是创建一个装饰器，它可以将函数的调用结果缓存起来，以便下次使用。

#### 步骤 1: 编写缓存装饰器函数

Python 标准库中提供了一个非常好用的装饰器，它就是 `functools` 模块中的 `@lru_cache`。`lru` 是 "Least Recently Used"（最近最少使用）的缩写，这意味着它会自动淘汰掉那些最不常用的缓存结果，以节省内存。

我们将使用 `@lru_cache` 来实现我们的缓存功能，并结合我们之前学习的计时装饰器，这样我们就能直观地看到缓存带来的性能提升。

```python
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
result_uncached = fibonacci(35)
print(f"结果: {result_uncached}")

print("---")
print("测试已缓存的斐波那契函数:")
result_cached = fibonacci_with_cache(35)
print(f"结果: {result_cached}")
print("再次调用相同参数，这次应该会很快:")
result_cached_again = fibonacci_with_cache(35)
print(f"结果: {result_cached_again}")
```

**设计思路解释：**

  * **`@functools.lru_cache(maxsize=None)`:** 这是 Python 内置的缓存装饰器。`maxsize=None` 意味着缓存没有大小限制，会一直保留结果。你也可以设置一个具体的整数，比如 `maxsize=128`，当缓存超过这个数量时，最近最少使用的缓存项会被移除。
  * **装饰器嵌套:** 注意 `fibonacci_with_cache` 函数上方的两个装饰器。`@lru_cache` 在内层，`@timer` 在外层。这意味着：
    1.  `@lru_cache` 会先作用于 `fibonacci_with_cache` 函数，为其添加缓存功能。
    2.  `@timer` 再作用于这个“带缓存功能的新函数”，为其添加计时功能。
    3.  因此，计时器会准确地计算**带缓存**的函数的执行时间。

-----

#### 步骤 2: 运行代码并观察效果

将上述代码复制到你的 Python 文件中并运行。

**执行结果示例：**

```
---
测试未缓存的斐波那契函数:
函数 'fibonacci' 执行耗时: 3.1234 秒
结果: 9227465
---
测试已缓存的斐波那契函数:
函数 'fibonacci_with_cache' 执行耗时: 0.0001 秒
结果: 9227465
再次调用相同参数，这次应该会很快:
函数 'fibonacci_with_cache' 执行耗时: 0.0000 秒
结果: 9227465
```

**结果分析：**

  * **未缓存的函数:** 计算 `fibonacci(35)` 耗时巨大（约 3 秒），因为函数中包含了大量的重复计算。
  * **已缓存的函数:** 第一次计算 `fibonacci_with_cache(35)` 的耗时显著降低（约 0.0001 秒），因为它会缓存子问题的结果，比如 `fibonacci_with_cache(33)` 和 `fibonacci_with_cache(34)`。
  * **再次调用:** 第二次调用 `fibonacci_with_cache(35)` 几乎不耗时（约 0.0000 秒），因为结果已经完全缓存下来了，程序直接返回了缓存中的值。

-----

### 总结

现在你已经掌握了如何用内置的 `@lru_cache` 装饰器来实现高性能的缓存功能。在算法和机器学习中，如果你有需要重复调用且输入固定的计算函数，使用这个装饰器能够带来巨大的性能提升。

接下来，你想继续学习关于装饰器的更多高级用法（比如**带参数的装饰器**），还是想继续学习下一个设计模式：**工厂模式**？