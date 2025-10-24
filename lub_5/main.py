from collections import deque

def gen_bin_tree(root, height, left = lambda lr: lr ** 3, right = lambda rr: (rr*2)-1):
    genroot = [root, None, None]

    if height == 1:
        return genroot

    # Очередь для вершин
    queue = deque([(genroot, 1)])
    while queue:
        node, level = queue.popleft()
        if level >= height:
            continue
        current_value = node[0]
        # Создание левой вершины
        left_value = left(current_value)
        left_child = [left_value, None, None]
        node[1] = left_child
        # Создание правой вершины
        right_value = right(current_value)
        right_child = [right_value, None, None]
        node[2] = right_child
        # Добавление вершин в список
        queue.append((left_child, level + 1))
        queue.append((right_child, level + 1))
    return genroot

print(gen_bin_tree(12,4))
