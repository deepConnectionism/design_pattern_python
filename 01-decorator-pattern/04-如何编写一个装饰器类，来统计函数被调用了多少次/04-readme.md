太棒了！既然你对装饰器充满兴趣，那我们来学习一个更面向对象的写法：**装饰器类**。

### 概略介绍解决方案

到目前为止，我们编写的装饰器都是函数。但在某些情况下，使用**类**来编写装饰器会更具优势，尤其当装饰器需要**维护状态**（state）时。

例如，我们想创建一个缓存装饰器，不仅要缓存函数的返回值，还要统计缓存的命中次数和未命中次数。用函数来实现会比较复杂，但用类来实现就非常自然，因为我们可以将这些统计数据作为类的属性来存储。

装饰器类的核心思想是：

1.  创建一个**类**，这个类的实例在被调用时，会像一个函数一样运行。
2.  这个类在初始化时接收**被装饰的函数**作为参数。
3.  它通过实现 `__call__` 方法，来定义在调用被装饰函数时的行为。

我们将通过一个具体的例子来学习：**如何编写一个装饰器类，来统计函数被调用了多少次。**

-----

### 代码和实现说明

我们的目标是创建一个名为 `CallCounter` 的装饰器类，它可以统计被装饰函数被调用的次数。

#### 步骤 1: 编写装饰器类

首先，我们来编写这个 `CallCounter` 类。

```python
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
```

**设计思路解释：**

  * **`__init__(self, func)`:** 这是类的构造函数。当我们将 `@CallCounter` 放在一个函数上方时，Python 会自动执行 `my_func = CallCounter(my_func)`。因此，`self.func` 就存储了被装饰的原始函数。
  * **`functools.update_wrapper(self, func)`:** 这个函数的作用与 `@functools.wraps` 装饰器相同，它能确保被装饰函数的元信息（如函数名、文档字符串）被正确地复制到我们的 `CallCounter` 实例上。
  * **`self.calls = 0`:** 我们在 `__init__` 方法中初始化了一个实例属性 `self.calls`，这就是我们用来**维护状态**的变量。每次调用函数时，我们都会更新这个属性。
  * **`__call__(self, *args, **kwargs)`:** 这是类装饰器的核心。当我们将 `my_func` 赋值为 `CallCounter(my_func)` 后，每次调用 `my_func()` 实际上都在调用 `CallCounter` 实例的 `__call__` 方法。我们在这里编写装饰器的实际逻辑。

-----

#### 2\. 应用装饰器类

现在我们有了 `CallCounter` 装饰器类，我们可以用它来装饰任何需要统计调用次数的函数。

```python
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
```

**如何实现：**

1.  将上述代码块复制到你的 Python 文件中。
2.  在 `add_numbers` 和 `say_hello` 函数上方加上 `@CallCounter`。
3.  运行代码，观察 `__call__` 方法中的打印语句如何随着每次调用而更新。

**执行结果示例：**

```
函数 'add_numbers' 被调用了 1 次
结果: 8
函数 'add_numbers' 被调用了 2 次
结果: 30
---
函数 'say_hello' 被调用了 1 次
结果: Hello!
函数 'say_hello' 被调用了 2 次
结果: Hello!
函数 'say_hello' 被调用了 3 次
结果: Hello!
add_numbers 函数总共被调用了 2 次。
```

-----

### 总结

现在你已经掌握了**装饰器类**的用法。相比于函数装饰器，类装饰器在需要**维护状态**或**更复杂的逻辑**时，提供了更清晰、更结构化的实现方式。

我们已经深入探讨了装饰器的核心概念、带参数的装饰器，以及装饰器类的实现。你已经对装饰器有了全面的理解。

接下来，你想继续学习下一个设计模式：**工厂模式**吗？这个模式在需要根据不同情况创建不同对象的算法项目中非常有用。