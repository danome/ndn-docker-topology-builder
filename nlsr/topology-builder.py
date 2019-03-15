from typing import List

from nlsr_builder import NlsrBuilder
from node import Node
from neighbor import Neighbor
from compose_builder import ComposeBuilder

def printTopology(nodes: List[Node]):
    for node in nodes:
        node.printNighbours()

def buildLinearTwoTopology():
    print("\n\nBuilding linear-two topology")
    # A <--10--> B 
    nodeA = Node("A")
    nodeB = Node("B")

    nodeA.addNeighbor(Neighbor(nodeB))

    nodeB.addNeighbor(Neighbor(nodeA))

    topologyName = "linear"
    nodes = [nodeA, nodeB]
    printTopology(nodes)
    NlsrBuilder(topologyName).buildNlsrFiles(nodes)
    ComposeBuilder(topologyName, nodes).buildComposeFile()


def buildLinearThreeTopology():
    print("\n\nBuilding linear-three topology")
    
    """
     A <--10--> B <--20--> C
                |
                10
                X
    """

    nodeA = Node("A")
    nodeB = Node("B")
    nodeC = Node("C")

    # Adding my local machine to the mix
    nodeX = Node("X")
    nodeX.addNeighbor(Neighbor(nodeB))

    nodeA.addNeighbor(Neighbor(nodeB))

    nodeB.addNeighbor(Neighbor(nodeA))
    nodeB.addNeighbor(Neighbor(nodeC))
    nodeB.addNeighbor(Neighbor(nodeX))

    nodeC.addNeighbor(Neighbor(nodeB))

    topologyName = "linear-three"
    nodes = [nodeA, nodeB, nodeC, nodeX]
    printTopology(nodes)
    NlsrBuilder(topologyName).buildNlsrFiles(nodes)
    ComposeBuilder(topologyName, nodes).buildComposeFile()



def buildSquareTopology():
    print("\n\nBuilding square topology")
    """
        A --- 10 --- B
        |            |   
        10           10
        |            |
        D --- 10 --- C
    """
    nodeA = Node("A")
    nodeB = Node("B")
    nodeC = Node("C")
    nodeD = Node("D")

    nodeA.addNeighbor(Neighbor(nodeB))
    nodeA.addNeighbor(Neighbor(nodeD))

    nodeB.addNeighbor(Neighbor(nodeC))
    nodeB.addNeighbor(Neighbor(nodeA))

    nodeC.addNeighbor(Neighbor(nodeD))
    nodeC.addNeighbor(Neighbor(nodeB))

    nodeD.addNeighbor(Neighbor(nodeA))
    nodeD.addNeighbor(Neighbor(nodeC))

    topologyName = "square"
    nodes = [nodeA, nodeB, nodeC, nodeD]
    printTopology(nodes)
    NlsrBuilder(topologyName).buildNlsrFiles(nodes)
    ComposeBuilder(topologyName, nodes).buildComposeFile()

def buildTreeTopology():
    print("\n\nBuilding tree topology")
    nodeA = Node("A")
    nodeB = Node("B")
    nodeC = Node("C")
    nodeD = Node("D")
    nodeE = Node("E", router=True)
    nodeF = Node("F", router=True)
    nodeG = Node("G", router=True)

    # Leaf nodes have a single parent
    nodeA.addNeighbor(Neighbor(nodeE))
    nodeB.addNeighbor(Neighbor(nodeE))
    nodeC.addNeighbor(Neighbor(nodeF))
    nodeD.addNeighbor(Neighbor(nodeF))

    # Root node has two connections
    nodeG.addNeighbor(Neighbor(nodeE))
    nodeG.addNeighbor(Neighbor(nodeF))

    # Intermediate Nodes have two children and one paerent
    nodeE.addNeighbor(Neighbor(nodeA))
    nodeE.addNeighbor(Neighbor(nodeB))
    nodeE.addNeighbor(Neighbor(nodeG))
    nodeF.addNeighbor(Neighbor(nodeC))
    nodeF.addNeighbor(Neighbor(nodeD))
    nodeF.addNeighbor(Neighbor(nodeG))

    topologyName = "tree"
    nodes = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]
    printTopology(nodes)
    NlsrBuilder(topologyName).buildNlsrFiles(nodes)
    ComposeBuilder(topologyName, nodes).buildComposeFile()


def buildFourChildTreeTopology():
    print("\n\nBuilding four-child-tree topology")
    nodeA = Node("A")
    nodeB = Node("B")
    nodeC = Node("C")
    nodeD = Node("D")
    nodeE = Node("E", router=True)

    # Add connection to parent
    nodeA.addNeighbor(Neighbor(nodeE))
    nodeB.addNeighbor(Neighbor(nodeE))
    nodeC.addNeighbor(Neighbor(nodeE))
    nodeD.addNeighbor(Neighbor(nodeE))
    
    # Add reverse connection
    nodeE.addNeighbor(Neighbor(nodeA))
    nodeE.addNeighbor(Neighbor(nodeB))
    nodeE.addNeighbor(Neighbor(nodeC))
    nodeE.addNeighbor(Neighbor(nodeD))

    topologyName = "four-child-tree"
    nodes = [nodeA, nodeB, nodeC, nodeD, nodeE]
    printTopology(nodes)
    NlsrBuilder(topologyName).buildNlsrFiles(nodes)
    ComposeBuilder(topologyName, nodes).buildComposeFile()


def buildDumbbellTopology():
    print("\n\nBuilding dumbbell topology")
    
    # Left side
    nodeA = Node("A")
    nodeB = Node("B")
    
    # Right side
    nodeC = Node("C")
    nodeD = Node("D")

    # Left router
    nodeE = Node("E", router=True)

    # Right router
    nodeF = Node("F", router=True)

    # Each of left nodes are connected to E
    nodeA.addNeighbor(Neighbor(nodeE))
    nodeB.addNeighbor(Neighbor(nodeE))

    # Each of right nodes are connected to F
    nodeC.addNeighbor(Neighbor(nodeF))
    nodeD.addNeighbor(Neighbor(nodeF))

    # E is connected to all left nodes and F
    nodeE.addNeighbor(Neighbor(nodeA))
    nodeE.addNeighbor(Neighbor(nodeB))
    nodeE.addNeighbor(Neighbor(nodeF))

    # F is connected to all right nodes and E
    nodeF.addNeighbor(Neighbor(nodeC))
    nodeF.addNeighbor(Neighbor(nodeD))
    nodeF.addNeighbor(Neighbor(nodeE))

    topologyName = "dumbbell"
    nodes = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF]
    printTopology(nodes)
    NlsrBuilder(topologyName).buildNlsrFiles(nodes)
    ComposeBuilder(topologyName, nodes).buildComposeFile()



if __name__ == '__main__':
    buildLinearTwoTopology()
    buildLinearThreeTopology()
    buildSquareTopology()
    buildTreeTopology()
    buildFourChildTreeTopology()
    buildDumbbellTopology()