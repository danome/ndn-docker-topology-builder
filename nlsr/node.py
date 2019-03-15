
class Node:

    def __init__(self, nodeId: str, router=False):
        self.nodeId = nodeId
        self.nodeName = "node" + nodeId
        self.hostName = "node" + nodeId.lower() + ".ndngame.com"
        self.neighborList = []
        self.router = router
    
    def addNeighbor(self, neighbor):
        self.neighborList.append(neighbor)
    
    def printNighbours(self):
        for neighbor in self.neighborList:
            print("{} <-{}-> {}".format(self.asString(), neighbor.linkCost, neighbor.node.asString()))
    
    def asString(self):
        gameNodeFormat = "{}({})"
        routerFormat = "{}_r({})"
        if (self.router):
            return routerFormat.format(self.nodeId, self.hostName)
        
        return gameNodeFormat.format(self.nodeId, self.hostName)