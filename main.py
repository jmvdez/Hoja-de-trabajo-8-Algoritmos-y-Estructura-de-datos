class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

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