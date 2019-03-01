from nlsr_builder import NlsrBuilder
from node import Node
from neighbor import Neighbor

ips = {
    "A": "172.19.0.10",
    "B": "172.19.0.11"
}

def buildLinearTwoTopology():
    # A <--10--> B 
    nodeA = Node("A", ips["A"])
    nodeB = Node("B", ips["B"])

    nodeA.addNeighbor(Neighbor(nodeB, 10))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeA, 10))
    nodeB.printNighbours()

    nlsr = NlsrBuilder("linear")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)


def buildLinearThreeTopology():
    # A <--10--> B <--20--> C
    nodeA = Node("A", "192.168.1.10")
    nodeB = Node("B", "192.168.1.11")
    nodeC = Node("C", "192.168.1.12")

    nodeA.addNeighbor(Neighbor(nodeB, 10))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeA, 10))
    nodeB.addNeighbor(Neighbor(nodeC, 20))
    nodeB.printNighbours()

    nodeC.addNeighbor(Neighbor(nodeB, 20))
    nodeC.printNighbours()

    nlsr = NlsrBuilder("linear-three")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)

def buildSquareTopology():
    """
        A --- 10 --- B
        |            |   
        10           10
        |            |
        D --- 10 --- C
    """
    nodeA = Node("A", "192.168.1.10")
    nodeB = Node("B", "192.168.1.11")
    nodeC = Node("C", "192.168.1.12")
    nodeD = Node("D", "192.168.1.13")

    nodeA.addNeighbor(Neighbor(nodeB, 10))
    nodeA.printNighbours()

    nodeB.addNeighbor(Neighbor(nodeC, 10))
    nodeB.printNighbours()

    nodeC.addNeighbor(Neighbor(nodeD, 10))
    nodeC.printNighbours()

    nodeD.addNeighbor(Neighbor(nodeA, 10))
    nodeD.printNighbours()

    nlsr = NlsrBuilder("square")
    nlsr.buildNlsrFile(nodeA)
    nlsr.buildNlsrFile(nodeB)
    nlsr.buildNlsrFile(nodeC)
    nlsr.buildNlsrFile(nodeD)

def buildTreeTopology():
    nodeA = Node("A", "192.168.1.10")
    nodeB = Node("B", "192.168.1.11")
    nodeC = Node("C", "192.168.1.12")
    nodeD = Node("D", "192.168.1.13")
    nodeE = Node("E", "192.168.1.14")
    nodeF = Node("F", "192.168.1.15")
    nodeG = Node("G", "192.168.1.16")

    nodeG.addNeighbor(Neighbour(nodeE, 10))
    nodeG.addNeighbor(Neighbour(nodeF, 10))

    nodeE.addNeighbor(Neighbour(nodeA, 10))
    nodeE.addNeighbor(Neighbour(nodeB, 10))

    nodeF.addNeighbor(Neighbour(nodeC, 10))
    nodeF.addNeighbor(Neighbour(nodeD, 10))


if __name__ == '__main__':
    buildLinearTwoTopology()