import networkx as nx
import matplotlib.pyplot as plt
import random

class Node:
    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None

    def insert(self, key):
        if key > self.key:
            if self.right is None:
                self.right = Node(key)
            else:
                self.right.insert(key)
        elif key < self.key:
            if self.left is None:
                self.left = Node(key)
            else:
                self.left.insert(key)

    def printTree(self):
        if self.left is not None:
            self.left.printTree()
        print(f'key: {self.key}')
        if self.right is not None:
            self.right.printTree()

    def getH(self):
        hR = -1 if self.right is None else self.right.getH()
        hL = -1 if self.left is None else self.left.getH()
        return 1 + max(hR, hL)


def setGrafi(node: Node, G):
    if node.left is not None:
        G.add_edge(node.key, node.left.key)
        setGrafi(node.left, G)
    if node.right is not None:
        G.add_edge(node.key, node.right.key)
        setGrafi(node.right, G)

def setPosition(node: Node, pos, n, x=0, y=0):
    pos[node.key] = x, y
    if node.left is not None:
        setPosition(node.left, pos, n, x - node.getH(), y - 2)
    if node.right is not None:
        setPosition(node.right, pos, n, x + node.getH(), y - 2)


def getNNodi(node: Node):
    if node is None:
        return 0
    return 1 + getNNodi(node.right) + getNNodi(node.left)

def main():
    lista = (list(range(0, 80, 5)))
    random.shuffle(lista)

    root = Node(lista[0])
    for n in lista[1:]:
        root.insert(n)

    G = nx.Graph()
    pos = {}
    print(getNNodi(root), 'h:', root.getH())

    setPosition(root, pos, getNNodi(root))
    setGrafi(root, G)

    print(f'pos: {pos}')
    options = {
        "font_size": 20,
        "node_size": 1000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 2,
        "width": 2
    }

    nx.draw_networkx(G, pos, **options)
    plt.show()


if __name__ == '__main__':
    main()
