from node import Node

class Neighbor:
    def __init__(self, node, linkCost=10):
        self.node = node
        self.linkCost = linkCost