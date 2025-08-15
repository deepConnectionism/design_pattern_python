太棒了！我们现在开始学习第一个设计模式：**装饰器模式 (Decorator Pattern)**。

### 概略介绍解决方案

**装饰器模式**是一种非常强大的设计模式，它的核心思想是在不改变原有函数或类的代码的情况下，动态地给它们添加新的功能。在 Python 中，装饰器模式通过 `@` 语法糖实现，这使得代码非常简洁且易于理解。

在你的算法和机器学习项目中，装饰器非常有用，比如：

  * **性能监控:** 计算一个函数（如模型训练、数据预处理）的执行时间。
  * **日志记录:** 记录函数的调用情况、输入参数和返回值。
  * **缓存:** 对于计算量大的函数，缓存其结果以避免重复计算。

我们将通过一个具体的例子来学习：**如何使用装饰器来计算一个函数运行所需的时间**。

-----

### 代码和实现说明

我们的目标是创建一个装饰器，它可以“包装”任何函数，并在该函数执行前后记录时间，最终打印出总耗时。

#### 步骤 1: 编写装饰器函数

首先，我们来编写一个名为 `timer` 的装饰器函数。

```python
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
```

**设计思路解释：**

  * **`timer(func)`:** 这是最外层的装饰器函数，它接受一个函数 `func` 作为参数，这个 `func` 就是被装饰的函数。
  * **`@functools.wraps(func)`:** 这是一个非常重要的细节。如果不使用它，被装饰的函数会丢失它本身的元信息（如函数名 `__name__` 和文档字符串 `__doc__`）。`@functools.wraps` 的作用是将被装饰函数的元信息复制到装饰器返回的 `wrapper` 函数上，这样我们就能在 `wrapper` 中正确地获取到原始函数的信息。
  * **`wrapper(*args, **kwargs)`:** 这是内部函数，它才是真正被调用的地方。`*args` 和 `**kwargs` 用于接收任意数量的位置参数和关键字参数，确保我们的装饰器可以应用于任何签名（参数列表）的函数。
  * **时间计算:** `time.perf_counter()` 提供了高精度的计时器，非常适合用来测量代码块的执行时间。
  * **返回结果:** `return result` 确保装饰器不会改变原始函数的返回值，这对于函数的正常执行至关重要。

-----

#### 步骤 2: 应用装饰器

现在我们有了 `timer` 装饰器，我们可以用它来装饰任何需要计时的函数。

```python
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
```

**如何实现：**

1.  将上述代码块复制到你的 Python 文件中。
2.  在 `my_complex_calculation` 和 `another_function` 上方加上 `@timer`。这个语法糖是 Python 自动执行 `my_complex_calculation = timer(my_complex_calculation)` 的简写形式。
3.  运行代码，你将看到函数执行前后的时间被自动记录和打印出来。

**执行结果示例：**

```
函数 'my_complex_calculation' 执行耗时: 2.0001 秒
计算完成！模拟耗时 2 秒。
---
函数 'another_function' 执行耗时: 0.5001 秒
8
```

-----

### 总结

现在你已经掌握了如何编写和使用一个简单的装饰器来计时。这个模式的强大之处在于它的**可复用性**和**非侵入性**。你可以创建一个用于日志记录的装饰器、一个用于参数验证的装饰器等等，然后通过一行 `@` 就能应用到任何函数上，而无需修改函数本身的逻辑。

接下来，你想学习如何用装饰器来实现**缓存**功能，还是想继续学习下一个设计模式：**工厂模式**？