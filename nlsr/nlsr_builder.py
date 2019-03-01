import os
from neighbor import Neighbor

logdir = "/logs/nlsr"

gamePrefix = "/com/stefanolupo/ndngame/0"
nameFormat = "node{nodeId}"

nlsrTemplateFile="./nlsr-template.conf"
nlsrOutputFormat="topologies/{topologyName}/{name}-nlsr.conf"

neighborFormat = \
"neighbor  {{\n\
    name /com/stefanolupo/%C1.Router/router{nodeId}\n\
    face-uri  udp4://{nodeIp}\n\
    link-cost {linkCost}\n\
}}\n\n"


advertisementsFormat = [
    "/discovery/broadcast",
    "/discovery/{name}",
    "/config/broadcast",
    "/config/{name}",

    "/{name}/blocks/sync",
    "/{name}/blocks/interact",
    "/{name}/status/sync",
]

def buildNeighbor(neighbor):
    node = neighbor.node
    return neighborFormat.format(nodeId=node.nodeId, nodeIp=node.nodeIp, linkCost=neighbor.linkCost)

def buildNeighbors(node):
    return "\n".join([buildNeighbor(neighbor) for neighbor in node.neighborList])

def buildAdvertisement(lst, **kwargs):
    return ["\tprefix " + gamePrefix + item.format(**kwargs) for item in lst]

def buildAdvertisements(nodeName):
    advertisements = "\n".join(buildAdvertisement(advertisementsFormat, name=nodeName))
    return "\n\t{}\n".format(advertisements)

class NlsrBuilder:
    def __init__(self, topologyName="out", maxFacesPerPrefix=0):
        self.maxFacesPerPrefix = maxFacesPerPrefix
        self.topologyName = topologyName
    
    def buildNlsrFile(self, node):
        # Template needs:
        #   nodeId (for my router name)
        #   logdir
        #   neighbours
        #   maxFacesPerPrefix
        #   advertising

        neighbors = buildNeighbors(node)
        nodeName = nameFormat.format(nodeId=node.nodeId)
        advertisements = buildAdvertisements(nodeName)

        with open(nlsrTemplateFile) as templateFile:
            template = templateFile.read()
            template = template.replace("<nodeId>", node.nodeId)
            template = template.replace("<logdir>", logdir)
            template = template.replace("<neighbors>", neighbors)
            template = template.replace("<maxFacesPerPrefix>", str(self.maxFacesPerPrefix))
            template = template.replace("<advertising>", advertisements)
        
        if not os.path.exists(self.topologyName):
            os.mkdir(self.topologyName)
        with open(nlsrOutputFormat.format(topologyName=self.topologyName, name=nodeName), 'w+') as outFile:
            outFile.write(template)

    def getNlsrFile(self):
        return nlsrOutputFormat.format()
