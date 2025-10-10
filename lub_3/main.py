#Root = 12; height = 4

def left(root):
    """Вычисляет значение левого потомка."""
    return root ** 3

def right(root):
    """Вычисляет значение правого потомка."""
    return (root * 2)-1

def gen_bin_tree(height, root, l_b=left, r_b=right):
    """Генерирует бинарное дерево в виде списка.

       Каждый узел: {значение: [левое_поддерево, правое_поддерево]}
       Листья: {значение: []}
       """
    if height == 0:
        return {root: []}
    left_d = l_b(root)
    right_d = r_b(root)
    l_s = gen_bin_tree(height - 1, left_d, l_b, r_b)
    r_s = gen_bin_tree(height - 1, right_d, l_b, r_b)
    return {root: [l_s, r_s]}
print (gen_bin_tree(5, 12))

def gen_bee_tree_dict(height, root, l_b=left, r_b=right):
    """Генерирует бинарное дерево в виде словаря.

        Каждый узел: {значение: {'left': левое_поддерево, 'right': правое_поддерево}}
        Листья: {значение: {}}
        """
    if height == 0:
        return {root: []}
    left_d = l_b(root)
    right_d = r_b(root)
    l_s = gen_bee_tree_dict(height - 1, left_d, l_b, r_b)
    r_s = gen_bee_tree_dict(height - 1, right_d, l_b, r_b)
    return {root: {'left': l_s, 'right': r_s}}



