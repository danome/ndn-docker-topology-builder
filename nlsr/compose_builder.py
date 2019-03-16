import os
from typing import List

from node import Node

COMPOSE_TEMPLATE = "templates/compose-template.yml"
SERVICE_TEMPLATE = "templates/service-template.yml"
COMPOSITIONS_DIR = "compositions"
COMPOSE_FILE_NAME = "docker-compose.yml"

GAME_JAR_DIR = "/home/stefano/projects/NdnGame/NdnGameLibGdxDesktop/build/libs"
GAME_JAR_TARGET = "/NdnGame"
gameJarVolume = "- {}:{}".format(GAME_JAR_DIR, GAME_JAR_TARGET)

NLSR_DIR = "/home/stefano/projects/ndn-script/nlsr/topologies"
NLSR_TARGET = "/NLSR"
nlsrVolume = "- {}:{}".format(NLSR_DIR, NLSR_TARGET)

GAME_COMMAND_FORMAT = "- GAME=java -jar /NdnGame/NdnGameLibGdxDesktop-1.0-SNAPSHOT.jar -a wsp -hl -n {nodeName}"
NLSR_CONFIG_FORMAT = "- NLSR_CONFIG=" + NLSR_TARGET + "/{topology}/{nodeName}-nlsr.conf"

with open(COMPOSE_TEMPLATE) as f: 
    composeFormat = "".join(f.readlines())
with open(SERVICE_TEMPLATE) as f: 
    serviceFormat = "".join(f.readlines())

class ComposeBuilder:
    def __init__(self, topology: str, nodes: List[Node]):
        self.topology = topology
        self.services = "".join([ServiceBuilder(topology, node).buildServiceString() for node in nodes])
    
    def buildComposeFile(self):
        composeFileString = composeFormat.format(services=self.services)
        directory = os.path.join(COMPOSITIONS_DIR, self.topology)
        os.makedirs(directory, exist_ok=True)
        filename = os.path.join(directory, COMPOSE_FILE_NAME)
        with open(filename, 'w+') as f:
            f.write(composeFileString)
        return composeFileString

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