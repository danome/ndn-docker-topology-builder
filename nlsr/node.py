from typing import List

from neighbor import Neighbor

class Node:

    def __init__(self, nodeId: str, router=False):
        self.nodeId = nodeId
        self.nodeName = "node" + nodeId
        self.hostname = "node" + nodeId.lower() + ".ndngame.com"
        self.neighborList: List[Neighbor] = []
        self.router = router
    
    def addNeighbor(self, neighbor: Neighbor):
        self.neighborList.append(neighbor)
    
    def printNighbours(self):
        for neighbor in self.neighborList:
            print("{} <-{}-> {}".format(self.__str__(), neighbor.linkCost, str(neighbor.node)))
    
    def __str__(self):
        gameNodeFormat = "{}({})"
        routerFormat = "{}_r({})"
        if (self.router):
            return routerFormat.format(self.nodeId, self.hostname)
        
        return gameNodeFormat.format(self.nodeId, self.hostname)