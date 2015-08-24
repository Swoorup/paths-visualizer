from os.path import isfile, join
from os import walk
from struct import unpack
from io import BytesIO
import re
import collections


class SAPathSingleNode:
    def __init__(self, node):
        self.path = BytesIO(open(node, "rb").read())
        self.__header = {}
        self.__pathnodes = []
        self.__carpathlinks = []
        self.__links = []
        self.__navi = []
        self.__linklengths = []
        self.__pathintersectionsflags = []
        self._offset = 20

        # headers
        self.__header['NumNodes'] = unpack('I', self.path.read(4))[0]
        self.__header['NumVehNodes'] = unpack('I', self.path.read(4))[0]
        self.__header['NumPedNodes'] = unpack('I', self.path.read(4))[0]
        self.__header['NumCarPathLinks'] = unpack('I', self.path.read(4))[0]
        self.__header['NumLinksArray'] = unpack('I', self.path.read(4))[0]

        self.__read_pathnodes()
        self.__read_carpathlinks()
        self.__read_links_array()
        self.__read_carpathlinks_array()
        self.__read_linklengths()
        self.__read_pathintersection_flags()

        # following sets uses NODE ID as a hash
        self.carPathNodes = collections.OrderedDict()
        self.carpathLinks = collections.OrderedDict();

        self.boatPathNodes = collections.OrderedDict()
        self.boatpathLinks = collections.OrderedDict();

        self.pedPathNodes = collections.OrderedDict()
        # end of key-value pairs

        self.__seperateNodes()
        self.__buildHierarchy()

    def __seperateNodes(self):
        for i in range(0, self.__header['NumVehNodes']):
            # cars and boats nodes

            # check if boat
            if (self.__pathnodes[i]['isWaterNode'] == False:
                self.carPathNodes[i] = self.__pathnodes[i]


    def __buildHierarchy(self):

        for i in range(self.__pathnodes):
            self.__pathnodes['_links'] = []

            for j in range(self.__pathnodes[i]['numberOfLinks']):
                linkedNode = self.__pathnodes[i]['baseLink'] + j
                address = self.__links[linkedNode]

                if i < self.__header['NumVehNodes']:
                    # vehicle
                    self.__pathnodes[i]['_links'].append = collections.OrderedDict({'type': "vehicle", 'carpathlink':'a'})

        # add linked nodes directly to pathnodes
        for node in self.__pathnodes:
            node["vectorLinks"] = []

            for i in range(node['numberOfLinks']):
                linkIndex = node['baseLink'] + i
                linkedNodeAddress = self.__links[linkIndex]

                # check node type
                if i < self.__header['NumVehNodes']:
                    carpathlink = self.__navi[linkIndex]
                    node["vectorLinks"].append(collections.OrderedDict({'CarPathLink' : carpathlink, 'linked': linkedNodeAddress}))
                else:
                    node["vectorLinks"].append(collections.OrderedDict({'linked':linkedNodeAddress}))

    def __read_pathnodes(self):
        if len(self.__pathnodes) != self.__header['NumNodes']:
            self.path.seek(self._offset, 0)
            for i in range(self.__header['NumNodes']):
                self.__pathnodes.append({})
                self.path.read(4)  # Memory Address
                self.path.read(4)  # Zero

                self.__pathnodes[i] = collections.OrderedDict()
                self.__pathnodes[i]['x'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.__pathnodes[i]['y'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.__pathnodes[i]['z'] = float(unpack('h', self.path.read(2))[0]) / 8

                self.path.read(2)  # heuristic path cost

                self.__pathnodes[i]['baseLink'] = unpack('h', self.path.read(2))[0]
                self.__pathnodes[i]['areaID'] = unpack('h', self.path.read(2))[0]
                self.__pathnodes[i]['nodeID'] = unpack('h', self.path.read(2))[0]
                self.__pathnodes[i]['width'] = unpack('b', self.path.read(1))[0] / 8
                self.__pathnodes[i]['floodcolor'] = unpack('b', self.path.read(1))[0]

                flags = unpack('B', self.path.read(1))[0]
                self.__pathnodes[i]['numberOfLinks'] = flags & 15;
                self.__pathnodes[i]['isDeadEnd'] = True if (flags >> 4) & 1 == 1 else False
                self.__pathnodes[i]['isIgnoredNode'] = True if (flags >> 5) & 1 == 1 else False
                self.__pathnodes[i]['isRoadBlock'] = True if (flags >> 6) & 1 == 1 else False
                self.__pathnodes[i]['isWaterNode'] = True if (flags >> 7) & 1 == 1 else False

                flags = unpack('B', self.path.read(1))[0]
                self.__pathnodes[i]['isEmergencyVehicleOnly'] = True if flags & 1 == 1 else False
                self.__pathnodes[i]['isRestrictedAccess'] = True if (flags >> 1) & 1 == 1 else False
                self.__pathnodes[i]['isDontWander'] = True if (flags >> 2) & 1 == 1 else False
                self.__pathnodes[i]['unk2'] = True if (flags >> 3) & 1 == 1 else False
                self.__pathnodes[i]['speedlimit'] = (flags >> 4) & 3
                self.__pathnodes[i]['unk3'] = True if (flags >> 6) & 1 == 1 else False
                self.__pathnodes[i]['unk4'] = True if (flags >> 7) & 1 == 1 else False

                flags = unpack('B', self.path.read(1))[0]
                self.__pathnodes[i]['spawnProbability'] = flags & 15
                self.__pathnodes[i]['behaviourType'] = (flags >> 4) & 15
                flags = unpack('B', self.path.read(1))[0]  # padding?
        return self.__pathnodes


    def __read_carpathlinks(self):
        if len(self.__carpathlinks) != self.__header['NumCarPathLinks']:
            self.path.seek(self._offset + (self.__header['NumNodes'] * 28), 0)
            for i in range(self.__header['NumCarPathLinks']):
                self.__carpathlinks.append({})
                self.__carpathlinks[i]['x'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.__carpathlinks[i]['y'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.__carpathlinks[i]['targetArea'] = unpack('h', self.path.read(2))[0]
                self.__carpathlinks[i]['targetNode'] = unpack('h', self.path.read(2))[0]
                self.__carpathlinks[i]['dirX'] = float(unpack('b', self.path.read(1))[0]) / 100
                self.__carpathlinks[i]['dirY'] = float(unpack('b', self.path.read(1))[0]) / 100

                self.__carpathlinks[i]['width'] = unpack('b', self.path.read(1))[0]

                flags = unpack('B', self.path.read(1))[0]
                self.__carpathlinks[i]['numLeftLanes'] = flags & 7
                self.__carpathlinks[i]['numRightLanes'] = (flags >> 3) & 7
                self.__carpathlinks[i]['trafficLight'] = (flags >> 4) & 1

                flags = unpack('B', self.path.read(1))[0]
                self.__carpathlinks[i]['trafficLightState'] = flags & 11
                self.__carpathlinks[i]['isTrainCrossing'] = (flags >> 2) & 1

                flags = unpack('B', self.path.read(1))[0]
        return self.__carpathlinks

    def __read_links_array(self):
        if len(self.__links) != self.__header['NumLinksArray']:
            self.path.seek(self._offset + (self.__header['NumNodes'] * 28) + (self.__header['NumCarPathLinks'] * 14), 0)
            for i in range(self.__header['NumLinksArray']):
                self.__links.append({})
                self.__links[i]['area'] = unpack('h', self.path.read(2))[0]
                self.__links[i]['node'] = unpack('h', self.path.read(2))[0]
        return self.__links


    def __read_carpathlinks_array(self):
        if len(self.__navi) != self.__header['NumLinksArray']:
            self.path.seek(self._offset + (self.__header['NumNodes'] * 28) + (self.__header['NumCarPathLinks'] * 14) + (self.__header['NumLinksArray'] * 4) + 768,0)
            for i in range(self.__header['NumLinksArray']):
                self.__navi.append({})
                carpathlinkaddress = unpack('H', self.path.read(2))[0]
                self.__navi[i]['carpathlink'] = carpathlinkaddress & 1023
                self.__navi[i]['area'] = carpathlinkaddress >> 10
        return self.__navi


    def __read_linklengths(self):
        if len(self.__linklengths) != self.__header['NumLinksArray']:
            self.path.seek(self._offset + (self.__header['NumNodes'] * 28) + (self.__header['NumCarPathLinks'] * 14) + (self.__header['NumLinksArray'] * 4) + 768 + (self.__header['NumLinksArray'] * 2), 0)
            for i in range(self.__header['NumLinksArray']):
                self.__linklengths.append(unpack('b', self.path.read(1))[0])
        return self.__linklengths

    # atm it seem buggy
    def __read_pathintersection_flags(self):
        if len(self.__pathintersectionsflags) != self.__header['NumPedNodes']:
            self.path.seek(self._offset + (self.__header['NumNodes'] * 28) + (self.__header['NumCarPathLinks'] * 14) + (self.__header['NumLinksArray'] * 4) + 768 + (self.__header['NumLinksArray'] * 2) + self.__header['NumLinksArray'], 0)
            for i in range(self.__header['NumLinksArray']):
                self.__pathintersectionsflags.append({})
                flags = unpack('B', self.path.read(1))[0]
                self.__pathintersectionsflags[i]['isRoadCross'] = True if flags & 1 else False
                self.__pathintersectionsflags[i]['isTrafficLight'] = True if flags & 2 else False

        return self.__pathintersectionsflags

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
            filepath = join(dirpath, i)
            print("[x] Opening file " + filepath)
            dict_path_files[area_id] = SAPathSingleNode(filepath)

        odict_path_files = collections.OrderedDict(sorted(dict_path_files.items()))

        # for each file
        for area, pathfile in odict_path_files.items():
            for i in pathfile.pathnodes:
                print(i)
            if len(pathfile.pathnodes) > 0:
                break


"""
        self.vehiclePathNodes.extend(pathfile.Paths()[:pathfile.numVehnodes])
        self.pedPathNodes.extend(pathfile.Paths()[pathfile.numVehnodes:pathfile.numNodes])
        self.numVehicleNodes += pathfile.numVehnodes
        self.numPedNodes += pathfile.numPednodes
                """
