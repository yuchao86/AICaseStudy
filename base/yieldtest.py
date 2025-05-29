
def simple_generator():
    yield 1
    yield 2
    yield 3


gen = simple_generator()

for value in gen:
    print(value)  # 依次输出: 1, 2, 3


def conditional_generator(limit):
    n = 0
    while n < limit:
        if n % 2 == 0:  # 只生成偶数
            yield n
        n += 1


gen_expr = (x for x in range(5) if x % 2 == 0)  # 生成0到4之间的偶数
for value in gen_expr:
    print(value)  # 输出: 0, 2, 4