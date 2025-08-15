import itertools

my_list = [1, 2, 3]
my_tuple = ('a', 'b', 'c')

# 将两个可迭代对象连接起来
combined_iterator = itertools.chain(my_list, my_tuple)
print("\n使用 itertools.chain() 串联结果:")
for item in combined_iterator:
    print(item, end=" ")

# 对迭代器进行切片
sliced_iterator = itertools.islice(range(10), 3, 7)
print("\n\n使用 itertools.islice() 切片结果:")
for item in sliced_iterator:
    print(item, end=" ")

print() 