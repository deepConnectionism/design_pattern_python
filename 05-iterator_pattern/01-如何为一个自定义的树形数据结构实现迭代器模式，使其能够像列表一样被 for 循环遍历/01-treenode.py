from collections import deque

# 在 TreeNode 类中添加 __iter__ 方法
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __iter__(self):
        # 返回一个迭代器实例
        return TreeNodeIterator(self)

    def __repr__(self):
        return f"TreeNode({self.value})"

class TreeNodeIterator:
    """
    一个实现了广度优先遍历 (BFS) 的迭代器。
    """
    def __init__(self, root: TreeNode):
        # 使用 deque 作为队列，来实现 BFS
        self._queue = deque([root])

    def __iter__(self):
        # 迭代器协议要求 __iter__ 返回自身
        return self

    def __next__(self):
        # 迭代器协议的核心方法
        if not self._queue:
            # 如果队列为空，则遍历结束，抛出 StopIteration 异常
            raise StopIteration
        
        # 从队列中取出下一个节点
        current_node = self._queue.popleft()
        
        # 将当前节点的所有子节点加入队列
        for child in current_node.children:
            self._queue.append(child)
            
        return current_node.value


# 客户端代码：创建树
root = TreeNode("A")
b = TreeNode("B")
c = TreeNode("C")
d = TreeNode("D")
e = TreeNode("E")
f = TreeNode("F")

root.add_child(b)
root.add_child(c)

b.add_child(d)
b.add_child(e)

c.add_child(f)

# 使用 for 循环遍历树
print("广度优先遍历 (BFS) 结果:")
for value in root:
    print(value, end=" ")
# 预期输出: A B C D E F

# 在 for 循环结束后，手动添加一个换行符, 否则当程序执行完毕后，命令行终端在没有收到换行符的情况下，会直接在当前行的末尾显示下一个提示符（比如 % 或 $）。
# 这个 % 符号通常是 Zsh（macOS 的默认 Shell）或者其他一些 Shell 的提示符，用来告诉你上一行没有以换行符结尾。
print() 