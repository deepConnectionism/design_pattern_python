class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    # 使用生成器来实现广度优先遍历 (BFS)
    def __iter__(self):
        queue = [self]
        while queue:
            current_node = queue.pop(0)
            yield current_node.value
            queue.extend(current_node.children)

# 客户端代码 (和之前一样)
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

print("使用生成器进行广度优先遍历 (BFS) 结果:")
for value in root:
    print(value, end=" ")

print() 