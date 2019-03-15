from typing import List

from node import Node

COMPOSE_TEMPLATE = "templates/compose-template.yml"
SERVICE_TEMPLATE = "templates/service-template.yml"

GAME_JAR_DIR = "/home/stefano/projects/NdnGame/NdnGameLibGdxDesktop/build/libs"
GAME_JAR_TARGET = "/NdnGame"
gameJarVolume = "{}:{}".format(GAME_JAR_DIR, GAME_JAR_TARGET)

NLSR_DIR = "/home/stefano/projects/ndn-script/nlsr/topologies"
NLSR_TARGET = "/NLSR"
nlsrVolume = "{}:{}".format(NLSR_DIR, NLSR_TARGET)

GAME_COMMAND_FORMAT = "- GAME=java -jar /NdnGame/NdnGameLibGdxDesktop-1.0-SNAPSHOT.jar -a wsp -hl -n {nodeName}"
NLSR_CONFIG_FORMAT = "- NLSR_CONFIG=" + NLSR_TARGET + "/{topology}/{nodeName}-nlsr.conf"

with open(COMPOSE_TEMPLATE) as f: 
    composeFormat = "".join(f.readlines())
with open(SERVICE_TEMPLATE) as f: 
    serviceFormat = "".join(f.readlines())

class ComposeBuilder:
    def __init__(self, topology: str, nodes: List[Node]):
        self.services = "".join([ServiceBuilder(topology, node).buildServiceString() for node in nodes])
        # print(self.services )
    
    def buildComposeFile(self):
        return composeFormat.format(services=self.services)

class ServiceBuilder:
    def __init__(self, topology: str, node: Node):
        self.node = node
        self.nlsrConfig = NLSR_CONFIG_FORMAT.format(topology=topology, nodeName=node.nodeName)
        self.gameCommand = "" if node.router else GAME_COMMAND_FORMAT.format(nodeName=node.nodeName)
    
    def buildServiceString(self) -> str:
        return serviceFormat.format(
            nodeId=self.node.nodeId, 
            nlsrConfig=self.nlsrConfig,
            gameCommand=self.gameCommand,
            gameJarVolume=gameJarVolume,
            nlsrVolume=nlsrVolume,
            nodeName=self.node.nodeName, 
            nodeHostname=self.node.hostname
        )

if __name__ == "__main__":
    composeBuilder = ComposeBuilder("tree", [Node("A"), Node("G", router=True)])
    print(composeBuilder.buildComposeFile())