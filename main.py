import random

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


def escenario_A_BST():
    bst = BST()

    values = [random.randint(1, 10000) for _ in range(1000)]

    for v in values:
        bst.insert(v)

    searches = random.sample(values, 100)

    total = 0
    for s in searches:
        _, it = bst.search(s)
        total += it

    return total / 100