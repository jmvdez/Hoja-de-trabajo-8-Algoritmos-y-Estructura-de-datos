import random
import matplotlib.pyplot as plt

# =========================
# BST
# =========================
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


# =========================
# SPLAY TREE
# =========================
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
        if not root or root.key == key:
            return root, counter

        counter += 1

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


# =========================
# RED BLACK TREE (simplificado)
# =========================
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


# =========================
# ESCENARIOS
# =========================

def escenario_A():
    bst, splay, rb = BST(), SplayTree(), RedBlackTree()

    values = [random.randint(1, 10000) for _ in range(1000)]

    for v in values:
        bst.insert(v)
        splay.insert(v)
        rb.insert(v)

    searches = random.sample(values, 100)

    return promedio_busqueda(bst, splay, rb, searches)


def escenario_B():
    bst, splay, rb = BST(), SplayTree(), RedBlackTree()

    values = list(range(1, 1001))  # ordenado

    for v in values:
        bst.insert(v)
        splay.insert(v)
        rb.insert(v)

    target = 1000

    return (
        bst.search(target)[1],
        splay.search(target)[1],
        rb.search(target)[1]
    )


def escenario_C():
    bst, splay, rb = BST(), SplayTree(), RedBlackTree()

    values = [random.randint(1, 10000) for _ in range(1000)]

    for v in values:
        bst.insert(v)
        splay.insert(v)
        rb.insert(v)

    target = values[0]

    bst_iter = []
    splay_iter = []
    rb_iter = []

    for _ in range(50):
        bst_iter.append(bst.search(target)[1])
        splay_iter.append(splay.search(target)[1])
        rb_iter.append(rb.search(target)[1])

    return (
        sum(bst_iter)/50,
        sum(splay_iter)/50,
        sum(rb_iter)/50
    )


def promedio_busqueda(bst, splay, rb, searches):
    bst_iter, splay_iter, rb_iter = [], [], []

    for s in searches:
        bst_iter.append(bst.search(s)[1])
        splay_iter.append(splay.search(s)[1])
        rb_iter.append(rb.search(s)[1])

    return (
        sum(bst_iter)/len(searches),
        sum(splay_iter)/len(searches),
        sum(rb_iter)/len(searches)
    )


# =========================
# GRAFICAS
# =========================

def graficar(A, B, C):
    labels = ["BST", "Splay", "RB"]

    x = range(len(labels))

    plt.figure(figsize=(10,6))

    plt.bar(x, A, alpha=0.5, label="Escenario A")
    plt.bar(x, B, alpha=0.5, label="Escenario B")
    plt.bar(x, C, alpha=0.5, label="Escenario C")

    plt.xticks(x, labels)
    plt.ylabel("Iteraciones")
    plt.title("Comparación de Árboles")
    plt.legend()
    plt.show()


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    A = escenario_A()
    B = escenario_B()
    C = escenario_C()

    print("\nEscenario A:", A)
    print("Escenario B:", B)
    print("Escenario C:", C)

    graficar(A, B, C)