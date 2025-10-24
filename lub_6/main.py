from collections import deque
import timeit
import matplotlib.pyplot as plt


def left(root):
    """Вычисляет значение левого потомка."""
    return root ** 3


def right(root):
    """Вычисляет значение правого потомка."""
    return (root * 2) - 1


def gen_bin_tree_recursive(height, root, l_b=left, r_b=right):
    """Генерирует бинарное дерево в виде списка."""
    if height == 0:
        return {root: []}
    left_d = l_b(root)
    right_d = r_b(root)
    l_s = gen_bin_tree_recursive(height - 1, left_d, l_b, r_b)
    r_s = gen_bin_tree_recursive(height - 1, right_d, l_b, r_b)
    return {root: [l_s, r_s]}


def gen_bin_tree_iterative(root, height, left=lambda lr: lr ** 3, right=lambda rr: (rr * 2) - 1):
    genroot = [root, None, None]
    if height == 1:
        return genroot
    queue = deque([(genroot, 1)])
    while queue:
        node, level = queue.popleft()
        if level >= height:
            continue
        current_value = node[0]
        left_value = left(current_value)
        left_child = [left_value, None, None]
        node[1] = left_child
        right_value = right(current_value)
        right_child = [right_value, None, None]
        node[2] = right_child
        queue.append((left_child, level + 1))
        queue.append((right_child, level + 1))
    return genroot


def benchmark(func, number=1, repeat=5):
    times = timeit.repeat(func, number=number, repeat=repeat)
    return min(times)


def main():
    test_data = list(range(13))

    iterative = []
    recursive = []

    for height in test_data:
        iterative_func = lambda h=height: gen_bin_tree_iterative(4, h)
        recursive_func = lambda h=height: gen_bin_tree_recursive(h, 4)
        iterative.append(benchmark(iterative_func))
        recursive.append(benchmark(recursive_func))

    # Визуализация
    plt.plot(test_data, iterative, label="Итеративное бинарное дерево")
    plt.plot(test_data, recursive, label='Рекурсивное бинарное дерево')
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение времени построения бинарных деревьев")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()