import bpy
import bmesh
from mathutils import Vector

from .ui_constants import *

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
    
# export VC PED PATH FOR NOW
def exportPedPaths(filepath, ob):
    print("Exporting to: " + filepath)
    print("Exporting Object: " + ob.name)
    file = open(filepath, 'w')
    file.write("path\n")
    me = ob.data
    
    # Get Bmesh representation
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    tagVerts = []
    tagEdges = []
    for i in range(len(bm.verts)):
        tagVerts.append({})
        tagVerts[i]['read'] = False
        tagVerts[i]['group'] = -1
        
    NumGroup = 0
    for i in range(len(bm.edges)):
        tagEdges.append({})
        tagEdges[i]['type'] = "none" # interna/external
        
    for v in bm.verts:
        if tagVerts[v.index]['read']:
            continue
            
        currentIndex = v.index
        internalNodes = []
        visitedNextNodes = []
        g = 0
        while True:
            assert len(bm.verts[currentIndex].link_edges) > 0
            
            nLinked = 0
            for link in bm.verts[currentIndex].link_edges:
                linkVert = link.other_vert( bm.verts[currentIndex] ).index
                  
                if tagVerts[linkVert]['group'] != NumGroup: 
                    nLinked += 1
                    
                    if tagVerts[linkVert]['group'] == -1:
                        visitedNextNodes.append(linkVert)
            
            if (g + nLinked + 1 <= 12):
                tagVerts[currentIndex]['group'] = NumGroup
                tagVerts[currentIndex]['read'] = True
            
                if currentIndex not in internalNodes:
                    internalNodes.append(currentIndex)
                    
                # values might be in the visited Next Nodes
                if currentIndex in visitedNextNodes:
                    visitedNextNodes.remove(currentIndex)
                    
                g += 1
                g = g + nLinked - 1
                if len(visitedNextNodes) == 0:
                    print("Failed LOL by " + str(currentIndex))
                    #Add search again? 
                    #if g < 12 search from a list
                    #TEST CODE
                    
                    #END TEST CODE
                    break
                else:
                    currentIndex = visitedNextNodes.pop()
            else:
                break
                
        print(internalNodes)
        #make sure list is unique
        assert len(internalNodes) == len(set(internalNodes))
        
        groupNodes = []
        for i in range(len(internalNodes)):
            groupNodes.append({})
            
            groupNodes[i]['realIndex'] = internalNodes[i]
            groupNodes[i]['xyz'] = bm.verts[internalNodes[i]].co
            groupNodes[i]['type'] = 2
            groupNodes[i]['next'] = -1
          
        for i in range(len(internalNodes)):
            for link in bm.verts[internalNodes[i]].link_edges:
                linkVert = link.other_vert( bm.verts[internalNodes[i]]).index
                    
                if tagVerts[linkVert]['group'] != NumGroup:
                    #externalNodes
                    externalNode = {}
                    externalNode['realIndex'] = linkVert
                    externalNode['xyz'] = (bm.verts[linkVert].co + bm.verts[internalNodes[i]].co)/2
                    externalNode['type'] = 1
                    externalNode['next'] = i
                    groupNodes.append(externalNode)
                else:
                    if groupNodes[internalNodes.index(linkVert)]['next'] != i and groupNodes[i]['next'] != internalNodes.index(linkVert):
                        groupNodes[internalNodes.index(linkVert)]['next'] = i
            
        # Adding padded nodes
        while len(groupNodes) != 12:
            ignoredNode = {}
            ignoredNode['type'] = 0
            ignoredNode['next'] = -1
            ignoredNode['xyz'] = Vector((0,0,0))
            groupNodes.append(ignoredNode)
            
        file.write("0, -1\n")
        #write relation
        for node in groupNodes:
            file.write( "\t{}, {}, {}, {:.2f}, {:.2f}, {:.2f}, {}, {}, {}, {}, {}, {}\n".format(
                node['type'], 
                node['next'], 
                0,
                node['xyz'].x * 16,
                node['xyz'].x * 16,
                node['xyz'].x * 16,
                2,
                1,
                1,
                1,
                0,
                1
                )
            )
            
        NumGroup += 1
                    
    bm.to_mesh(me)
    bm.free()
    file.write("end\n")
    file.close()
    
def PrepareJunctionOrSingleConnectionGroup(bm, groupNodes) : 
    groupNodes[0]['next'] = -1 # first node as internal
    groupNodes[0]['type'] = 2 # first node as internal
    groupNodes[0]['speedlimit'] = bm.verts[groupNodes[0]['realIndex']][bm.verts.layers.int[NODE_SPEEDLIMIT]]
    groupNodes[0]['flags'] = 0
    groupNodes[0]['spawnrate'] = bm.verts[groupNodes[0]['realIndex']][bm.verts.layers.int[NODE_SPAWNPROBABILITY]] / 15.0
    
    groupNodes[0]['median'] = 0 #these are ignored anyway
    groupNodes[0]['rightLanes'] = 0 #these are ignored anyway
    groupNodes[0]['leftLanes'] = 0 #these are ignored anyway
    
    # loop through all external nodes
    for i in range(1, len(groupNodes)):
        bm_edge = bm.edges.get(( bm.verts[ groupNodes[0]['realIndex'] ], bm.verts[ groupNodes[i]['realIndex'] ] ))
        toVert = bm_edge.verts[0]
        fromVert = bm_edge.verts[1]
        
        # external Nodes has to point to internal node
        node = groupNodes[i]
        if node['realIndex'] == fromVert.index:
            # already pointing
            node['leftLanes'] = bm_edge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]
            node['rightLanes'] = bm_edge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]
        else: 
            node['rightLanes'] = bm_edge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]
            node['leftLanes'] = bm_edge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]
        
        node['next'] = 0
        node['type'] = 1
        node['median'] = bm.verts[node['realIndex']][bm.verts.layers.float[NODE_WIDTH]]
        node['speedlimit'] = bm.verts[node['realIndex']][bm.verts.layers.int[NODE_SPEEDLIMIT]]
        node['flags'] = 0
        node['spawnrate'] = bm.verts[node['realIndex']][bm.verts.layers.int[NODE_SPAWNPROBABILITY]] / 15.0
        
        
    while len(groupNodes) != 12:
        ignoredNode = {}
        ignoredNode['type'] = 0
        ignoredNode['next'] = -1
        ignoredNode['xyz'] = Vector((0,0,0))
        ignoredNode['median'] = 0
        ignoredNode['speedlimit'] = 0
        ignoredNode['flags'] = 0
        ignoredNode['spawnrate'] = 0
        ignoredNode['median'] = 0 #these are ignored anyway
        ignoredNode['rightLanes'] = 0 #these are ignored anyway
        ignoredNode['leftLanes'] = 0 #these are ignored anyway
        ignoredNode['realIndex'] = -1 #these are ignored anyway
        groupNodes.append(ignoredNode)
        
def PrepareVehicleLineSegmentsGroup(bm, tempGroupNodes):
    
    groupNodes = []
    
    for lineVert in tempGroupNodes:
        pass
        
    
    return groupNodes
    
    
def exportVehiclePaths(filepath, ob, bIsWater):
    print("Exporting to: " + filepath)
    print("Exporting Object: " + ob.name)
    file = open(filepath, 'w')
    file.write("path\n")
    me = ob.data
    
    # Get Bmesh representation
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    
    tagVerts = []
    tagEdges = []
    for i in range(len(bm.verts)):
        tagVerts.append({})
        tagVerts[i]['read'] = False
        tagVerts[i]['type'] = "none"
        
    NumGroup = 0
        
    # find all junctions and single linked connections first
    for v in bm.verts:
        if tagVerts[v.index]['type'] == "internal":
            continue
            
        assert len(v.link_edges) > 0
        
        # skip all lines
        if len(v.link_edges) == 2:
            continue
        
        tagVerts[v.index]['type'] = "internal"
        
        
        lineSegments = []
        
        junctionOrSingleCenter = {}
        junctionOrSingleCenter['realIndex'] = v.index
        junctionOrSingleCenter['xyz'] = v.co
        
        groupNodes = []
        groupNodes.append(junctionOrSingleCenter)
        
        for link in v.link_edges:
            linkVert = link.other_vert(v).index
                
            # if link is part of a line, mark it as external node
            if len(bm.verts[linkVert].link_edges) == 2:                 
                tagVerts[linkVert]['type'] = "external"
                lineSegments.append(linkVert)
                
                extNode = {}
                extNode['xyz'] = bm.verts[linkVert].co
                extNode['realIndex'] = linkVert
                groupNodes.append(extNode)
            else:
                # this could be another junction or single linked node
                # in this case, get the middle point as external Node
                extNode = {}
                extNode['xyz'] = (bm.verts[linkVert].co + bm.verts[v.index].co)/2
                extNode['realIndex'] = linkVert
                
                groupNodes.append(extNode)
         
        # Now write the junction or singly linked connection
        PrepareJunctionOrSingleConnectionGroup(bm, groupNodes)
        file.write(str(2 if bIsWater else 1) + ", -1\n")
        for node in groupNodes:
            file.write( "\t{}, {}, {}, {:.2f}, {:.2f}, {:.2f}, {}, {}, {}, {}, {}, {}\n".format(
                node['type'], 
                node['next'], 
                0,
                node['xyz'].x * 16,
                node['xyz'].x * 16,
                node['xyz'].x * 16,
                node['median'],
                node['leftLanes'],
                node['rightLanes'],
                node['speedlimit'],
                node['flags'],
                node['spawnrate']
                )
            )
        
        # now start exporting all the line segments for that junction/single connection
        while len(lineSegments) > 0:
            lineStart = lineSegments.pop()
            
            assert tagVerts[lineStart]['type'] == "external"
            
            # keep on adding until a junction or singly connection has been reached
            lineNodes = []
            
            prevNode = v.index
            currentNode = lineStart
            
            while True:
                if len(bm.verts[currentNode].link_edges) != 2:
                    break
                else:
                    lineNodes.append(currentNode)
                    
                    # Also mark the nodes as internal
                    tagVerts[currentNode]['type'] = "internal"
                    
                nextVert = bm.verts[currentNode].link_edges[0].other_vert(bm.verts[currentNode]).index
                if nextVert == prevNode:
                    nextVert = bm.verts[currentNode].link_edges[1].other_vert(bm.verts[currentNode]).index
                
                prevNode = currentNode
                currentNode = nextVert
            
            assert len(lineNodes) >= 2
            
            # mark first and last as external
            tagVerts[lineNodes[0]]['type'] = "external"
            tagVerts[lineNodes[ len(lineNodes) -1 ]]['type'] = "external"
            
            if len(lineNodes) == 2:
                continue
            
            assert len(lineNodes) == len(set(lineNodes))
            
            lineGroups = []
            
            # start break down into group segments and write to the file
            tempGroupNodes = []
            nthGroup = 1
            maxNodes = 12
            for i in range(len(lineNodes)):         
                
                if len(lineNodes) - (nthGroup * maxNodes) == 1:
                    maxNodes -= 1
                    print("fuck", maxNodes)
                
                tempGroupNodes.append(node) 
                if len(tempGroupNodes) == maxNodes:
                    lineGroups.append(PrepareVehicleLineSegmentsGroup(bm, tempGroupNodes))
                    nthGroup += 1
                    tempGroupNodes = []
                    tempGroupNodes.append(node)
                        
                    
            assert len(tempGroupNodes) != 2
            
            #TESTCODE
            print (lineNodes)
            #END TEST CODE
            
        
        #TEST CODE
        for l in groupNodes:
            print(l)
        print(
"""
import bpy
import bmesh
#get attribute
obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

for v in bm.verts:
    v.select = False

"""
        )
        for i in groupNodes:
            if i['realIndex'] != - 1:
                print ("bm.verts[", i['realIndex'], "].select = True")
        
        #END TEST 
                    
    bm.to_mesh(me)
    bm.free()
    file.write("end\n")
    file.close()
