import matplotlib.pyplot as plt
import networkx as nx

# 定义设计模式分类与英文名称
patterns_en = {
    "Creational": [
        "Singleton", "Factory Method", "Abstract Factory", "Builder", "Prototype"
    ],
    "Structural": [
        "Adapter", "Bridge", "Composite", "Decorator", "Facade", "Flyweight", "Proxy"
    ],
    "Behavioral": [
        "Chain of Responsibility", "Command", "Interpreter", "Iterator", "Mediator",
        "Memento", "Observer", "State", "Strategy", "Template Method", "Visitor"
    ]
}

# 常用模式标记（1=高频，0=低频）
common_usage_en = {
    "Singleton": 1, "Factory Method": 1, "Abstract Factory": 1, "Strategy": 1,
    "Observer": 1, "Proxy": 1, "Decorator": 1, "Template Method": 1, "Adapter": 1
}

# 创建图
G = nx.Graph()

# 添加节点
for category, pats in patterns_en.items():
    G.add_node(category, type="category")
    for p in pats:
        G.add_node(p, type="pattern", common=common_usage_en.get(p, 0))
        G.add_edge(category, p)

# 布局
pos = nx.spring_layout(G, seed=42, k=0.7)

# 绘制
plt.figure(figsize=(12, 8))
colors = []
sizes = []
for node in G.nodes():
    if G.nodes[node]['type'] == "category":
        colors.append("#ffcc00")  # 类别颜色
        sizes.append(2000)
    else:
        if G.nodes[node]['common'] == 1:
            colors.append("#66ccff")  # 高频模式颜色
            sizes.append(1200)
        else:
            colors.append("#cccccc")  # 普通模式颜色
            sizes.append(900)

nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes, edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=10)
nx.draw_networkx_edges(G, pos)

plt.title("23 Design Patterns Overview (Common Patterns Highlighted)", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()
