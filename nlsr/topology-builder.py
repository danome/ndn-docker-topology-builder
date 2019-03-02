from nlsr_builder import NlsrBuilder
from node import Node
from neighbor import Neighbor

ips = {
    "A": "172.19.0.10",
    "B": "172.19.0.11",
    "C": "172.19.0.12",
    "D": "172.19.0.13",
    "E": "172.19.0.14",
    "F": "172.19.0.15",
    "G": "172.19.0.16",
    "X": "192.168.1.10"
}

def buildNode(nodeName):
    if nodeName not in ips:
        raise KeyError("{} is not in ips: {}".format(nodeName, ips))
    return Node(nodeName, ips[nodeName])

def buildLinearTwoTopology():
    print("\n\nBuilding linear-two topology")
    # A <--10--> B 
    nodeA = buildNode("A")
    nodeB = buildNode("B")

    nodeA.addNeighbor(Neighbor(nodeB, 10))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeA, 10))
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
    nodeX.addNeighbor(Neighbor(nodeB, 10))
    nodeX.printNighbours()

    nodeA.addNeighbor(Neighbor(nodeB, 10))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeA, 10))
    nodeB.addNeighbor(Neighbor(nodeC, 10))
    nodeB.addNeighbor(Neighbor(nodeX, 10))
    nodeB.printNighbours()

    nodeC.addNeighbor(Neighbor(nodeB, 10))
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

    nodeA.addNeighbor(Neighbor(nodeB, 10))
    nodeA.addNeighbor(Neighbor(nodeD, 10))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeC, 10))
    nodeB.addNeighbor(Neighbor(nodeA, 10))
    nodeB.printNighbours()

    nodeC.addNeighbor(Neighbor(nodeD, 10))
    nodeC.addNeighbor(Neighbor(nodeB, 10))
    nodeC.printNighbours()

    nodeD.addNeighbor(Neighbor(nodeA, 10))
    nodeD.addNeighbor(Neighbor(nodeC, 10))
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
    nodeE = buildNode("E")
    nodeF = buildNode("F")
    nodeG = buildNode("G")

    # Leaf nodes have a single parent
    nodeA.addNeighbor(Neighbor(nodeE, 10))
    nodeB.addNeighbor(Neighbor(nodeE, 10))
    nodeC.addNeighbor(Neighbor(nodeF, 10))
    nodeD.addNeighbor(Neighbor(nodeF, 10))

    # Root node has two connections
    nodeG.addNeighbor(Neighbor(nodeE, 10))
    nodeG.addNeighbor(Neighbor(nodeF, 10))

    # Intermediate Nodes have two children and one paerent
    nodeE.addNeighbor(Neighbor(nodeA, 10))
    nodeE.addNeighbor(Neighbor(nodeB, 10))
    nodeE.addNeighbor(Neighbor(nodeG, 10))
    nodeF.addNeighbor(Neighbor(nodeC, 10))
    nodeF.addNeighbor(Neighbor(nodeD, 10))
    nodeF.addNeighbor(Neighbor(nodeG, 10))

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


if __name__ == '__main__':
    buildLinearTwoTopology()
    buildLinearThreeTopology()
    buildSquareTopology()
    buildTreeTopology()