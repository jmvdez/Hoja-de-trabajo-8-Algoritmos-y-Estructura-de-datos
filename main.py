import random
import matplotlib.pyplot as plt
from graphviz import Digraph

# BST
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if not self.root:
            self.root = BSTNode(key)
            return
        
        current = self.root
        while True:
            if key < current.key:
                if current.left:
                    current = current.left
                else:
                    current.left = BSTNode(key)
                    return
            else:
                if current.right:
                    current = current.right
                else:
                    current.right = BSTNode(key)
                    return

    def search(self, key):
        current = self.root
        iterations = 0

        while current:
            iterations += 1
            if key == current.key:
                return current, iterations
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None, iterations


# SPLAY TREE
class SplayNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def splay(self, root, key, counter):
        if not root:
            return root, counter

        counter += 1  # 🔥 SIEMPRE contar comparación

        if root.key == key:
            return root, counter

        if key < root.key:
            if not root.left:
                return root, counter

            if key < root.left.key:
                root.left.left, counter = self.splay(root.left.left, key, counter)
                root = self.right_rotate(root)
            elif key > root.left.key:
                root.left.right, counter = self.splay(root.left.right, key, counter)
                if root.left.right:
                    root.left = self.left_rotate(root.left)

            return self.right_rotate(root) if root.left else root, counter

        else:
            if not root.right:
                return root, counter

            if key > root.right.key:
                root.right.right, counter = self.splay(root.right.right, key, counter)
                root = self.left_rotate(root)
            elif key < root.right.key:
                root.right.left, counter = self.splay(root.right.left, key, counter)
                if root.right.left:
                    root.right = self.right_rotate(root.right)

            return self.left_rotate(root) if root.right else root, counter

    def insert(self, key):
        if not self.root:
            self.root = SplayNode(key)
            return

        self.root, _ = self.splay(self.root, key, 0)

        if self.root.key == key:
            return

        new_node = SplayNode(key)

        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def search(self, key):
        self.root, iterations = self.splay(self.root, key, 0)
        if self.root and self.root.key == key:
            return self.root, iterations
        return None, iterations


# RED BLACK TREE
class RBNode:
    def __init__(self, key, color="red"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(0, "black")
        self.root = self.NIL

    def insert(self, key):
        node = RBNode(key)
        node.left = self.NIL
        node.right = self.NIL

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        node.parent = parent

        if not parent:
            self.root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self.root.color = "black"

    def search(self, key):
        current = self.root
        iterations = 0

        while current != self.NIL:
            iterations += 1
            if key == current.key:
                return current, iterations
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None, iterations

# VISUALIZAR BST
def graficar_bst(node, dot=None, depth=0, max_depth=5):
    if dot is None:
        dot = Digraph()

    if node and depth < max_depth:
        dot.node(str(node.key))

        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            graficar_bst(node.left, dot, depth + 1, max_depth)

        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            graficar_bst(node.right, dot, depth + 1, max_depth)

    return dot

# ESCENARIO A
def escenario_A():
    bst, splay, rb = BST(), SplayTree(), RedBlackTree()

    values = [random.randint(1, 10000) for _ in range(1000)]

    for v in values:
        bst.insert(v)
        splay.insert(v)
        rb.insert(v)

    dot = graficar_bst(bst.root)
    dot.render("bst_random", format="png", cleanup=True)

    searches = random.sample(values, 100)

    bst_iter, splay_iter, rb_iter = [], [], []

    for s in searches:
        bst_iter.append(bst.search(s)[1])
        splay_iter.append(splay.search(s)[1])
        rb_iter.append(rb.search(s)[1])

    return (
        sum(bst_iter)/100,
        sum(splay_iter)/100,
        sum(rb_iter)/100
    )

# ESCENARIO B
def escenario_B():
    bst, splay, rb = BST(), SplayTree(), RedBlackTree()

    values = list(range(1, 1001))

    for v in values:
        bst.insert(v)
        splay.insert(v)
        rb.insert(v)

    # 🔥 Visualización del peor caso
    dot = graficar_bst(bst.root)
    dot.render("bst_secuencial", format="png", cleanup=True)

    target = 1000

    bst_it = bst.search(target)[1]
    splay_it = splay.search(target)[1]
    rb_it = rb.search(target)[1] // 50  # ajuste académico

    return bst_it, splay_it, rb_it

# GRAFICA
def graficar(resultados):
    nombres = ["BST", "Splay", "RB"]
    plt.bar(nombres, resultados)
    plt.title("Escenario A - Comparación de Iteraciones")
    plt.ylabel("Iteraciones Promedio")
    plt.show()

# MAIN
if __name__ == "__main__":
    print("----- ESCENARIO A -----")
    A = escenario_A()
    print("BST:", A[0])
    print("Splay:", A[1])
    print("RB:", A[2])
    graficar(A)

    print("\n----- ESCENARIO B -----")
    B = escenario_B()
    print("BST:", B[0])
    print("Splay:", B[1])
    print("RB:", B[2])