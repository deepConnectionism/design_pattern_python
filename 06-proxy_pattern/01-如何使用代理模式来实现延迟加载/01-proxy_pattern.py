from abc import ABC, abstractmethod
import time

# 定义一个昂贵的对象接口
class Image(ABC):
    """昂贵对象的抽象接口。"""
    @abstractmethod
    def display(self):
        """显示图片。"""
        pass

# 昂贵的原始对象
class LargeImage(Image):
    """一个创建和加载过程非常耗时的类。"""
    def __init__(self, filename):
        print(f"正在从硬盘加载 {filename}...")
        time.sleep(2)  # 模拟加载耗时
        self.filename = filename

    def display(self):
        print(f"正在显示 {self.filename}...")

# 代理对象
class ImageProxy(Image):
    """为 LargeImage 提供延迟加载的代理。"""
    def __init__(self, filename):
        self.filename = filename
        self._image = None  # 原始对象的引用，初始为 None

    def display(self):
        # 核心逻辑：只有在第一次调用 display() 时才创建原始对象
        if self._image is None:
            print("代理对象发现原始对象不存在，正在创建它...")
            self._image = LargeImage(self.filename)
        
        # 将请求转发给原始对象
        self._image.display()

# 客户端代码
print("客户端启动，准备创建代理对象...")
# 客户端创建代理对象，而不是原始对象
image_proxy = ImageProxy("test_image.jpg")
print("代理对象已创建，但原始对象还未加载。")

print("---")

print("客户端第一次请求显示图片...")
# 第一次调用 display()，代理会创建并加载原始对象
image_proxy.display()

print("---")

print("客户端第二次请求显示图片...")
# 第二次调用 display()，代理会直接将请求转发给已创建的原始对象
image_proxy.display()