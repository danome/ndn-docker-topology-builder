from nlsr_builder import NlsrBuilder
from node import Node
from neighbor import Neighbor

# ips = {
#     "A": "172.19.0.10",
#     "B": "172.19.0.11",
#     "C": "172.19.0.12",
#     "D": "172.19.0.13",
#     "E": "172.19.0.14",
#     "F": "172.19.0.15",
#     "G": "172.19.0.16",
#     "X": "192.168.1.10"
# }


def buildNode(nodeName, router=False):
    # if nodeName not in ips:
    #     raise KeyError("{} is not in ips: {}".format(nodeName, ips))
    hostname = "node" + nodeName.lower() + ".ndngame.com"
    return Node(nodeName, hostname, router=router)

def buildLinearTwoTopology():
    print("\n\nBuilding linear-two topology")
    # A <--10--> B 
    nodeA = buildNode("A")
    nodeB = buildNode("B")

    nodeA.addNeighbor(Neighbor(nodeB))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeA))
    nodeB.printNighbours()

    nlsr = NlsrBuilder("linear")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)


def buildLinearThreeTopology():
    print("\n\nBuilding linear-three topology")
    
    """
     A <--10--> B <--20--> C
                |
                10
                X
    """

    nodeA = buildNode("A")
    nodeB = buildNode("B")
    nodeC = buildNode("C")

    # Adding my local machine to the mix
    nodeX = buildNode("X")
    nodeX.addNeighbor(Neighbor(nodeB))
    nodeX.printNighbours()

    nodeA.addNeighbor(Neighbor(nodeB))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeA))
    nodeB.addNeighbor(Neighbor(nodeC))
    nodeB.addNeighbor(Neighbor(nodeX))
    nodeB.printNighbours()

    nodeC.addNeighbor(Neighbor(nodeB))
    nodeC.printNighbours()

    nlsr = NlsrBuilder("linear-three")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)
    nlsr.buildNlsrFile(nodeX)



def buildSquareTopology():
    print("\n\nBuilding square topology")
    """
        A --- 10 --- B
        |            |   
        10           10
        |            |
        D --- 10 --- C
    """
    nodeA = buildNode("A")
    nodeB = buildNode("B")
    nodeC = buildNode("C")
    nodeD = buildNode("D")

    nodeA.addNeighbor(Neighbor(nodeB))
    nodeA.addNeighbor(Neighbor(nodeD))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeC))
    nodeB.addNeighbor(Neighbor(nodeA))
    nodeB.printNighbours()

    nodeC.addNeighbor(Neighbor(nodeD))
    nodeC.addNeighbor(Neighbor(nodeB))
    nodeC.printNighbours()

    nodeD.addNeighbor(Neighbor(nodeA))
    nodeD.addNeighbor(Neighbor(nodeC))
    nodeD.printNighbours()

    nlsr = NlsrBuilder("square")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)
    nlsr.buildNlsrFile(nodeD)

def buildTreeTopology():
    print("\n\nBuilding tree topology")
    nodeA = buildNode("A")
    nodeB = buildNode("B")
    nodeC = buildNode("C")
    nodeD = buildNode("D")
    nodeE = buildNode("E", router=True)
    nodeF = buildNode("F", router=True)
    nodeG = buildNode("G", router=True)

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

    nodeA.printNighbours()
    nodeB.printNighbours()
    nodeC.printNighbours()
    nodeD.printNighbours()
    nodeE.printNighbours()
    nodeF.printNighbours()
    nodeG.printNighbours()

    nlsr = NlsrBuilder("tree")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)
    nlsr.buildNlsrFile(nodeD)
    nlsr.buildNlsrFile(nodeE)
    nlsr.buildNlsrFile(nodeF)
    nlsr.buildNlsrFile(nodeG)


def buildFourChildTreeTopology():
    print("\n\nBuilding four-child-tree topology")
    nodeA = buildNode("A")
    nodeB = buildNode("B")
    nodeC = buildNode("C")
    nodeD = buildNode("D")
    nodeE = buildNode("E", router=True)

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

    nodeA.printNighbours()
    nodeB.printNighbours()
    nodeC.printNighbours()
    nodeD.printNighbours()
    nodeE.printNighbours()

    nlsr = NlsrBuilder("four-child-tree")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)
    nlsr.buildNlsrFile(nodeD)
    nlsr.buildNlsrFile(nodeE)


def buildDumbbellTopology():
    print("\n\nBuilding dumbbell topology")
    
    # Left side
    nodeA = buildNode("A")
    nodeB = buildNode("B")
    
    # Right side
    nodeC = buildNode("C")
    nodeD = buildNode("D")

    # Left router
    nodeE = buildNode("E", router=True)

    # Right router
    nodeF = buildNode("F", router=True)

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

    nodeA.printNighbours()
    nodeB.printNighbours()
    nodeC.printNighbours()
    nodeD.printNighbours()
    nodeE.printNighbours()
    nodeF.printNighbours()

    nlsr = NlsrBuilder("dumbbell")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)
    nlsr.buildNlsrFile(nodeD)
    nlsr.buildNlsrFile(nodeE)
    nlsr.buildNlsrFile(nodeF)



if __name__ == '__main__':
    buildLinearTwoTopology()
    buildLinearThreeTopology()
    buildSquareTopology()
    buildTreeTopology()
    buildFourChildTreeTopology()
    buildDumbbellTopology()