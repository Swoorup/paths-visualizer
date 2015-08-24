from os.path import isfile, join
from os import walk
from struct import unpack
from io import BytesIO
import re
import collections

class NodeAddress:
    def __init__(self):
        self.areaID = -1
        self.nodeID = -1

class PathNode:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.baseLink = -1
        self.nodeAddress = NodeAddress()
        
        self.width = 0
        self.floodcolor = -1
        self.numberOfLinks = 0
        
        self.isDeadEnd  = False
        self.isIgnoredNode  = False
        self.isRoadBlock = False
        self.isWaterNode = False
        
        self.isEmergencyVehicleOnly = False
        self.isRestrictedAccess = False
        self.isDontWander = False
        self.unk2 = False
        
        self.speedlimit = 0
        self.unk3 = False
        self.unk4 = False
        
        self.spawnProbability = 0
        self.behaviourType = 0

        self.links = collections.OrderedDict()

class CarPathLink:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.linkedNodeAddress = NodeAddress()
        self.dirX = 0.0
        self.dirY = 0.0
        self.width = 0
        self.numLeftLanes = 0
        self.numRightLanes = 0
        self.trafficLight = 0
        
        self.trafficLightState = 0
        self.isTrainCrossing = 0
        

class SAPathSingleNode():
    def __init__(self, node):
        self.path = BytesIO(open(node, "rb").read())
        
        self.pathnodes = []
        self.navinodes = []
        self.links = []
        self.navilinks = []
        self.linklengths = []
        self._offset = 20
        
        # headers
        self.numNodes     = unpack('I', self.path.read(4))[0]
        self.numVehnodes     = unpack('I', self.path.read(4))[0]
        self.numPednodes     = unpack('I', self.path.read(4))[0]
        self.numNavinodes = unpack('I', self.path.read(4))[0]
        self.numLinks     = unpack('I', self.path.read(4))[0]
    
    def Paths(self):
        if len(self.pathnodes) != self.numNodes:
            self.path.seek(self._offset, 0)
            for i in range(self.numNodes):
                node = PathNode()
                
                self.path.read(4) # Memory Address
                self.path.read(4) # Zero
                
                node.x = float(unpack('h', self.path.read(2))[0]) / 8
                node.y = float(unpack('h', self.path.read(2))[0]) / 8
                node.z = float(unpack('h', self.path.read(2))[0]) / 8
                self.path.read(2) # heuristic path cost
                
                node.baseLink =  unpack('h', self.path.read(2))[0]
                node.nodeAddress.areaID = unpack('h', self.path.read(2))[0]
                node.nodeAddress.nodeID = unpack('h', self.path.read(2))[0]
                node.width = unpack('b', self.path.read(1))[0] / 8
                node.floodcolor = unpack('b', self.path.read(1))[0]
                
                flags = unpack('B', self.path.read(1))[0]
                node.numberOfLinks = flags & 15;
                
                if (flags >> 4) & 1 == 1:
                    node.isDeadEnd = True
                if (flags >> 5) & 1 == 1:
                    node.isIgnoredNode = True
                if (flags >> 6) & 1 == 1:
                    node.isRoadBlock = True
                if (flags >> 7) & 1 == 1:
                    node.isWaterNode = True
                
                flags = unpack('B', self.path.read(1))[0]
                if flags & 1 == 1:
                    node.isEmergencyVehicleOnly = True
                if (flags >> 1) & 1 == 1:
                    node.isRestrictedAccess = True
                if (flags >> 2) & 1 == 1:
                    node.isDontWander = True
                if (flags >> 3) & 1 == 1:
                    node.unk2 = True
                node.speedlimit = (flags >> 4) & 3 
                if (flags >> 6) & 1 == 1:
                    node.unk3 = True
                if (flags >> 7) & 1 == 1:
                    node.unk4 = True
                
                flags = unpack('B', self.path.read(1))[0]
                node.spawnProbability = flags & 15
                node.behaviourType = (flags >> 4 )& 15
                
                flags = unpack('B', self.path.read(1))[0] # padding?
                
                self.pathnodes.append(node)
                
        return self.pathnodes
            
    def NaviNodes(self):
        if len(self.navinodes) != self.numNavinodes:
            self.path.seek(self._offset + (self.numNodes * 28), 0)
            for i in range(self.numNavinodes):
                carpathlink = CarPathLink()
                carpathlink.x = float(unpack('h', self.path.read(2))[0]) / 8
                carpathlink.y = float(unpack('h', self.path.read(2))[0]) / 8
                carpathlink.linkedNodeAddress.areaID =  unpack('h', self.path.read(2))[0]
                carpathlink.linkedNodeAddress.nodeID =  unpack('h', self.path.read(2))[0]
                carpathlink.dirX = float(unpack('b', self.path.read(1))[0]) / 100
                carpathlink.dirY = float(unpack('b', self.path.read(1))[0]) / 100

                carpathlink.width = unpack('b', self.path.read(1))[0]
                
                flags =  unpack('B', self.path.read(1))[0]
                carpathlink.numLeftLanes = flags & 7
                carpathlink.numRightLanes = (flags >> 3) & 7
                carpathlink.trafficLight = (flags >> 4) & 1
                
                flags =  unpack('B', self.path.read(1))[0]
                carpathlink.trafficLightState = flags & 11
                carpathlink.isTrainCrossing = (flags >> 2) & 1

                flags =  unpack('B', self.path.read(1))[0]
                self.navinodes.append(carpathlink)
        return self.navinodes
        
    def Links(self):
        if len(self.links) != self.numLinks:
            self.path.seek(self._offset + (self.numNodes * 28) + (self.numNavinodes * 14), 0)
            for i in range(self.numLinks):
                self.links.append({})
                self.links[i]['area'] = unpack('h', self.path.read(2))[0]
                self.links[i]['node'] = unpack('h', self.path.read(2))[0]
        return self.links
        
    def NaviLinks(self):
        if len(self.navilinks) != self.numLinks:
            self.path.seek(self._offset + (self.numNodes * 28) + (self.numNavinodes * 14) + (self.numLinks * 4) + 768, 0)
            for i in range(self.numLinks):
                self.navilinks.append({})
                carpathlinkaddress = unpack('h', self.path.read(2))[0]
                self.navilinks[i]['carpathlink'] = carpathlinkaddress & 1023
                self.navilinks[i]['area'] = carpathlinkaddress >> 10
        return self.navilinks
    
    def LinkLengths(self):
        if len(self.linklengths) != self.numLinks:
            self.path.seek(self._offset + (self.numNodes * 28) + (self.numNavinodes * 14) + (self.numLinks * 4) + 768 + (self.numLinks * 2), 0)
            for i in range(self.numLinks):
                self.linklengths.append(unpack('b', self.path.read(1))[0])
        return self.linklengths
        
    def Close(self):
        self.path.close()


class SAPaths:

    def __init__(self):
        self.vehiclePathNodes = collections.OrderedDict()
        self.pedPathNodes = collections.OrderedDict()

    def load_from_directory(self, dirpath):
        f = []
        for (dirpath, dirnames, filenames) in walk(dirpath):
            f.extend(filenames)
            break

        dict_path_files = {}
        for i in (files for files in f if files.lower().startswith("nodes") and files.lower().endswith(".dat")):
            area_id = int(re.search(r'\d+', i).group())
            dict_path_files[area_id] = SAPathSingleNode(join(dirpath, i))

        odict_path_files = collections.OrderedDict(sorted(dict_path_files.items()))

        # for each file
        for area, pathfile in odict_path_files.items():
            for i in range(pathfile.numVehnodes):

                # add node
                pathnode = pathfile.Paths()[i]

                # add its connection
                for j in range(pathnode.numberOfLinks):
                    nextLinkAddress = pathfile.Links()[pathnode.baseLink + j]

                    print (nextLinkAddress)

                self.vehiclePathNodes[pathnode.nodeAddress] = pathnode

"""
        self.vehiclePathNodes.extend(pathfile.Paths()[:pathfile.numVehnodes])
        self.pedPathNodes.extend(pathfile.Paths()[pathfile.numVehnodes:pathfile.numNodes])
        self.numVehicleNodes += pathfile.numVehnodes
        self.numPedNodes += pathfile.numPednodes
                """