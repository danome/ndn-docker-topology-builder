
class Node:

    def __init__(self, nodeId, nodeIp):
        self.nodeId = nodeId
        self.nodeIp = nodeIp
        self.neighborList = []
    
    def addNeighbor(self, neighbor):
        self.neighborList.append(neighbor)
    
    def printNighbours(self):
        for neighbor in self.neighborList:
            print("{} <-{}-> {}".format(self.asString(), neighbor.linkCost, neighbor.node.asString()))
    
    def asString(self):
        return "{}({})".format(self.nodeId, self.nodeIp)