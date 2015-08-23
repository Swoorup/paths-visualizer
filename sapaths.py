from os.path import isfile, join
from os import walk
from struct import unpack
from io import BytesIO

class PathNode:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.baseLink = -1
        self.areaID = -1
        self.nodeID = -1
        
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

class CarPathLink:
    def __init__(self):
        self.x =  0.0
        self.y = 0.0

class SAPathSingleArea():
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
                node.areaID = unpack('h', self.path.read(2))[0]
                node.nodeID = unpack('h', self.path.read(2))[0]
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
                self.navinodes.append({})
                self.navinodes[i]['x']        = float(unpack('h', self.path.read(2))[0]) / 8
                self.navinodes[i]['y']        = float(unpack('h', self.path.read(2))[0]) / 8
                self.navinodes[i]['area']    = unpack('h', self.path.read(2))[0]
                self.navinodes[i]['node']    = unpack('h', self.path.read(2))[0]
                self.navinodes[i]['disx']    = float(unpack('b', self.path.read(1))[0]) / 8
                self.navinodes[i]['disy']    = float(unpack('b', self.path.read(1))[0]) / 8
                self.navinodes[i]['flags']    = unpack('I', self.path.read(4))[0]
        return self.navinodes
        
    def Links(self):
        if len(self.links) != self.numLinks:
            self.path.seek(self._offset + (self.numNodes * 28) + (self.numNavinodes * 14), 0)
            for i in range(self.numLinks):
                self.links.append({})
                self.links[i]['area']    = unpack('h', self.path.read(2))[0]
                self.links[i]['node']    = unpack('h', self.path.read(2))[0]
        return self.links
        
    def NaviLinks(self):
        if len(self.navilinks) != self.numLinks:
            self.path.seek(self._offset + (self.numNodes * 28) + (self.numNavinodes * 14) + (self.numLinks * 4) + 768, 0)
            for i in range(self.numLinks):
                self.navilinks.append(unpack('h', self.path.read(2))[0])
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
        self.vehiclePathNodes = []
        self.pedPathNodes = []
        self.numVehicleNodes = 0
        self.numPedNodes = 0
    
    def LoadFromDirectory(self, dirpath):
        f = []
        for (dirpath, dirnames, filenames) in walk(dirpath):
            f.extend(filenames)
            break
        
        for i in f:
            if i.lower().startswith("nodes") and i.lower().endswith(".dat"):
                pathfile = SAPathSingleArea(join(dirpath, i));
                self.vehiclePathNodes.extend(pathfile.Paths()[:pathfile.numVehnodes])
                self.pedPathNodes.extend(pathfile.Paths()[pathfile.numVehnodes:pathfile.numNodes])
                self.numVehicleNodes += pathfile.numVehnodes
                self.numPedNodes += pathfile.numPednodes
                