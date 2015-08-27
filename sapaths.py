from os.path import isfile, join
from os import walk
from struct import unpack
from io import BytesIO
import re
import collections
from time import sleep

class SAPathSingleNode:
    def __init__(self, node):
        self.path = BytesIO(open(node, "rb").read())
        self.mHeader = {}
        self.mPathnodes = []
        self.mCarpathlinks = []
        self.mLinks = []
        self.mNavi = []
        self.mLinklengths = []
        self.mPathintersectionsflags = []
        self.___offfset = 20

        # headers
        self.mHeader['NumNodes'] = unpack('I', self.path.read(4))[0]
        self.mHeader['NumVehNodes'] = unpack('I', self.path.read(4))[0]
        self.mHeader['NumPedNodes'] = unpack('I', self.path.read(4))[0]
        self.mHeader['NumCarPathLinks'] = unpack('I', self.path.read(4))[0]
        self.mHeader['NumLinksArray'] = unpack('I', self.path.read(4))[0]

        self.__read_pathnodes()
        self.__read_carpathlinks()
        self.__read_links_array()
        self.__read_carpathlinks_array()
        self.__read_linklengths()
        self.__read_pathintersection_flags()


    def __read_pathnodes(self):
        if len(self.mPathnodes) != self.mHeader['NumNodes']:
            self.path.seek(self.___offfset, 0)
            for i in range(self.mHeader['NumNodes']):
                self.mPathnodes.append({})
                self.path.read(4)  # Memory Address
                self.path.read(4)  # Zero

                self.mPathnodes[i] = collections.OrderedDict()
                self.mPathnodes[i]['x'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.mPathnodes[i]['y'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.mPathnodes[i]['z'] = float(unpack('h', self.path.read(2))[0]) / 8

                self.path.read(2)  # heuristic path cost

                self.mPathnodes[i]['baseLink'] = unpack('h', self.path.read(2))[0]
                self.mPathnodes[i]['areaID'] = unpack('h', self.path.read(2))[0]
                self.mPathnodes[i]['nodeID'] = unpack('h', self.path.read(2))[0]
                self.mPathnodes[i]['width'] = unpack('b', self.path.read(1))[0] / 8
                self.mPathnodes[i]['floodcolor'] = unpack('b', self.path.read(1))[0]

                flags = unpack('B', self.path.read(1))[0]
                self.mPathnodes[i]['numberOfLinks'] = flags & 15;
                self.mPathnodes[i]['isDeadEnd'] = True if (flags >> 4) & 1 == 1 else False
                self.mPathnodes[i]['isIgnoredNode'] = True if (flags >> 5) & 1 == 1 else False
                self.mPathnodes[i]['isRoadBlock'] = True if (flags >> 6) & 1 == 1 else False
                self.mPathnodes[i]['isWaterNode'] = True if (flags >> 7) & 1 == 1 else False

                flags = unpack('B', self.path.read(1))[0]
                self.mPathnodes[i]['isEmergencyVehicleOnly'] = True if flags & 1 == 1 else False
                self.mPathnodes[i]['isRestrictedAccess'] = True if (flags >> 1) & 1 == 1 else False
                self.mPathnodes[i]['isDontWander'] = True if (flags >> 2) & 1 == 1 else False
                self.mPathnodes[i]['unk2'] = True if (flags >> 3) & 1 == 1 else False
                self.mPathnodes[i]['speedlimit'] = (flags >> 4) & 3
                self.mPathnodes[i]['unk3'] = True if (flags >> 6) & 1 == 1 else False
                self.mPathnodes[i]['unk4'] = True if (flags >> 7) & 1 == 1 else False

                flags = unpack('B', self.path.read(1))[0]
                self.mPathnodes[i]['spawnProbability'] = flags & 15
                self.mPathnodes[i]['behaviourType'] = (flags >> 4) & 15
                flags = unpack('B', self.path.read(1))[0]  # padding?

                # blender specific
                self.mPathnodes[i]['_btraversed'] = False
        return self.mPathnodes


    def __read_carpathlinks(self):
        if len(self.mCarpathlinks) != self.mHeader['NumCarPathLinks']:
            self.path.seek(self.___offfset + (self.mHeader['NumNodes'] * 28), 0)
            for i in range(self.mHeader['NumCarPathLinks']):
                self.mCarpathlinks.append({})
                self.mCarpathlinks[i]['x'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.mCarpathlinks[i]['y'] = float(unpack('h', self.path.read(2))[0]) / 8
                self.mCarpathlinks[i]['targetArea'] = unpack('h', self.path.read(2))[0]
                self.mCarpathlinks[i]['targetNode'] = unpack('h', self.path.read(2))[0]
                self.mCarpathlinks[i]['dirX'] = float(unpack('b', self.path.read(1))[0]) / 100
                self.mCarpathlinks[i]['dirY'] = float(unpack('b', self.path.read(1))[0]) / 100

                self.mCarpathlinks[i]['width'] = unpack('b', self.path.read(1))[0]

                flags = unpack('B', self.path.read(1))[0]
                self.mCarpathlinks[i]['numLeftLanes'] = flags & 7
                self.mCarpathlinks[i]['numRightLanes'] = (flags >> 3) & 7
                self.mCarpathlinks[i]['trafficLight'] = (flags >> 4) & 1

                flags = unpack('B', self.path.read(1))[0]
                self.mCarpathlinks[i]['trafficLightState'] = flags & 11
                self.mCarpathlinks[i]['isTrainCrossing'] = (flags >> 2) & 1

                flags = unpack('B', self.path.read(1))[0]
        return self.mCarpathlinks

    def __read_links_array(self):
        if len(self.mLinks) != self.mHeader['NumLinksArray']:
            self.path.seek(self.___offfset + (self.mHeader['NumNodes'] * 28) + (self.mHeader['NumCarPathLinks'] * 14), 0)
            for i in range(self.mHeader['NumLinksArray']):
                self.mLinks.append({})
                self.mLinks[i]['area'] = unpack('h', self.path.read(2))[0]
                self.mLinks[i]['node'] = unpack('h', self.path.read(2))[0]
        return self.mLinks


    def __read_carpathlinks_array(self):
        if len(self.mNavi) != self.mHeader['NumLinksArray']:
            self.path.seek(self.___offfset + (self.mHeader['NumNodes'] * 28) + (self.mHeader['NumCarPathLinks'] * 14) + (self.mHeader['NumLinksArray'] * 4) + 768,0)
            for i in range(self.mHeader['NumLinksArray']):
                self.mNavi.append({})
                carpathlinkaddress = unpack('H', self.path.read(2))[0]
                self.mNavi[i]['carpathlink'] = carpathlinkaddress & 1023
                self.mNavi[i]['area'] = carpathlinkaddress >> 10
        return self.mNavi


    def __read_linklengths(self):
        if len(self.mLinklengths) != self.mHeader['NumLinksArray']:
            self.path.seek(self.___offfset + (self.mHeader['NumNodes'] * 28) + (self.mHeader['NumCarPathLinks'] * 14) + (self.mHeader['NumLinksArray'] * 4) + 768 + (self.mHeader['NumLinksArray'] * 2), 0)
            for i in range(self.mHeader['NumLinksArray']):
                self.mLinklengths.append(unpack('b', self.path.read(1))[0])
        return self.mLinklengths

    # atm it seem buggy
    def __read_pathintersection_flags(self):
        if len(self.mPathintersectionsflags) != self.mHeader['NumLinksArray']:
            self.path.seek(self.___offfset + (self.mHeader['NumNodes'] * 28) + (self.mHeader['NumCarPathLinks'] * 14) + (self.mHeader['NumLinksArray'] * 4) + 768 + (self.mHeader['NumLinksArray'] * 2) + self.mHeader['NumLinksArray'], 0)
            for i in range(self.mHeader['NumLinksArray']):
                self.mPathintersectionsflags.append({})
                flags = unpack('B', self.path.read(1))[0]
                self.mPathintersectionsflags[i]['isRoadCross'] = True if flags & 1 else False
                self.mPathintersectionsflags[i]['isTrafficLight'] = True if flags & 2 else False

        return self.mPathintersectionsflags

    def Close(self):
        self.path.close()


class SAPaths:
    def __init__(self):
        self.nodes = []
        self.carpathlinks = []

    @staticmethod
    def __validateCarPathLink(self, ListNodes, ListCarPathLinks):
        for node in ListNodes:
            nodeID = ListNodes.index(node)
            if node['_nodeType'] == 'ped':
                continue

            for link in node['_links']:
                linkNode = ListNodes[link['targetID']]
                assert node['isWaterNode'] == linkNode['isWaterNode']
                carpathlink = ListCarPathLinks[link['carpathlinkID']]
                assert nodeID >= carpathlink['targetID']
                if nodeID != carpathlink['targetID']: assert(link['targetID'] == carpathlink['targetID'])
        print("[x] Finished Validation: Check for assertion errors")

    @staticmethod
    def unify_all_nodes(self, dictionaryAreaFile):
        list_all_nodes = []
        list_all_carpathlinks = []

        hash_node_id = {}
        hash_carpathlink_id = {}

        for area, file_node in dictionaryAreaFile.items():
            # add all nodes
            for i in range(file_node.mHeader['NumNodes']):
                node = file_node.mPathnodes[i]
                hash_node_id[(area, node['nodeID'])] = len(list_all_nodes)

                # delete it as they are not used anymore
                del node['areaID']
                del node['nodeID']

                node['_links'] = []
                for k in range(node['numberOfLinks']):
                    connectioninfo = {
                        'target':               file_node.mLinks[node['baseLink'] + k],
                        'navilink':             file_node.mNavi[node['baseLink'] + k],
                        'length':               file_node.mLinklengths[node['baseLink'] + k],
                        'intersection':         file_node.mPathintersectionsflags[node['baseLink'] + k],
                    }
                    node['_links'].append(connectioninfo)

                del node['numberOfLinks']
                del node['baseLink']
                node['_nodeType'] = 'vehicle' if i < file_node.mHeader['NumVehNodes'] else 'ped'
                list_all_nodes.append(node)

            for i in range(file_node.mHeader['NumCarPathLinks']):
                carpathlink = file_node.mCarpathlinks[i]
                hash_carpathlink_id[(area, i)] = len(list_all_carpathlinks)
                list_all_carpathlinks.append(carpathlink)

        # assign the single IDs now, its better to let python do this stuff
        for i in range(len(list_all_nodes)):
            for k in range(len(list_all_nodes[i]['_links'])):
                list_all_nodes[i]['_links'][k]['targetID'] = hash_node_id[(list_all_nodes[i]['_links'][k]['target']['area'],list_all_nodes[i]['_links'][k]['target']['node'])]
                del list_all_nodes[i]['_links'][k]['target']

                # Only vehicle can have the car path links
                if list_all_nodes[i]['_nodeType'] == 'vehicle':
                    list_all_nodes[i]['_links'][k]['carpathlinkID'] = hash_carpathlink_id[(list_all_nodes[i]['_links'][k]['navilink']['area'], list_all_nodes[i]['_links'][k]['navilink']['carpathlink'])]

                del list_all_nodes[i]['_links'][k]['navilink']
                # del allNodes[i]['_links'][k]['navilink']

        # fix IDs in carpathlinks
        for i in range(len(list_all_carpathlinks)):
            list_all_carpathlinks[i]['targetID'] = hash_node_id[(list_all_carpathlinks[i]['targetArea'], list_all_carpathlinks[i]['targetNode'])]
            del list_all_carpathlinks[i]['targetNode']
            del list_all_carpathlinks[i]['targetArea']

        # Optional validation
        #self.__validateCarPathLink(self, list_all_nodes, list_all_carpathlinks)

        self.nodes = list_all_nodes
        self.carpathlinks = list_all_carpathlinks
        # next search of line segments

    def load_nodes_from_directory(self, dirpath):
        f = []
        for (dirpath, dirnames, filenames) in walk(dirpath):
            f.extend(filenames)
            break

        dict_path_files = {}
        for i in (files for files in f if files.lower().startswith("nodes") and files.lower().endswith(".dat")):
            area_id = int(re.search(r'\d+', i).group())
            filepath = join(dirpath, i)
            dict_path_files[area_id] = SAPathSingleNode(filepath)

        odict_path_files = collections.OrderedDict(sorted(dict_path_files.items()))

        self.unify_all_nodes(self, odict_path_files)
