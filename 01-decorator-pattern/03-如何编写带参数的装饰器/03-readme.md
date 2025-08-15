好的，我们继续深入学习装饰器！既然你已经掌握了基本的装饰器和内置的 `@lru_cache`，那我们来学习一个更高级、更强大的用法：**带参数的装饰器**。

### 概略介绍解决方案

我们之前写的装饰器，比如 `@timer`，是一个不带参数的装饰器。它总是以相同的方式工作。但在很多情况下，我们希望装饰器的行为是可以定制的。

例如：

  * 我们的计时器只打印到小数点后四位，但我们可能希望它能打印到任意精度。
  * 我们的 `@lru_cache` 没有大小限制，但我们可能希望为不同的函数设置不同的缓存大小。
  * 我们可能希望创建一个带参数的权限检查装饰器，比如 `@permission_required('admin')`。

**带参数的装饰器**就是为了解决这种需求而存在的。它实际上是**三层嵌套**的函数结构，最外层接收装饰器的参数，返回一个装饰器（也就是我们之前学的两层嵌套结构）。

我们将通过一个具体的例子来学习：**如何编写一个带参数的计时装饰器，让我们可以自定义打印精度。**

-----

### 代码和实现说明

我们的目标是创建一个名为 `timer_with_precision` 的装饰器，它可以像 `@timer_with_precision(precision=6)` 这样被调用，从而控制打印耗时的小数位数。

#### 步骤 1: 编写带参数的装饰器函数

带参数的装饰器需要一个额外的最外层函数来接收参数。

```python
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
```

**设计思路解释：**

  * **`timer_with_precision(precision=4)`:** 这是最外层的函数，它接收我们想要传递给装饰器的参数（这里是 `precision`）。它不直接返回 `wrapper`，而是返回 `decorator` 这个内部函数。
  * **`decorator(func)`:** 这是第二层函数，它的作用和我们之前写的 `@timer` 装饰器完全一样。它接收被装饰的函数 `func`，并返回 `wrapper` 函数。
  * **`wrapper(*args, **kwargs)`:** 这是最内层的函数，负责执行实际的逻辑。注意 `print` 语句中的 `{run_time:.{precision}f}`，我们通过 `precision` 参数来动态地控制格式化输出的精度。

-----

#### 步骤 2: 应用带参数的装饰器

现在我们有了 `timer_with_precision` 装饰器，我们可以在使用它时传入参数。

```python
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
```

**如何实现：**

1.  将上述代码复制到你的 Python 文件中。
2.  在函数上方使用 `@timer_with_precision(...)` 语法。注意，即使你使用默认参数，也需要加上括号，如 `@timer_with_precision()`。
3.  运行代码，观察不同精度的计时结果。

**执行结果示例：**

```
---
测试高精度计时:
函数 'my_complex_calculation_6_precision' 执行耗时: 0.149174 秒
计算完成！
---
测试默认精度计时:
函数 'my_complex_calculation_default_precision' 执行耗时: 0.1489 秒
计算完成！
```

-----

### 总结

现在你已经掌握了如何编写**带参数的装饰器**，这让你的装饰器更加灵活和可定制。这种模式在你的算法项目中非常有用，你可以编写各种带参数的装饰器来实现参数验证、权限检查等功能。

接下来，你想学习最后一个关于装饰器的话题：**如何编写装饰器类**，还是想继续学习下一个设计模式：**工厂模式**？