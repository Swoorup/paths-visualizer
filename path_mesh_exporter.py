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
def exportPaths(filepath, ob):
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
        g = 0
        while True:
            assert len(bm.verts[currentIndex].link_edges) > 0
            
            nextInternal = -1
            nLinked = 0
            for link in bm.verts[currentIndex].link_edges:
                
                linkVert = link.verts[0].index
                if linkVert == currentIndex:
                    linkVert = link.verts[1].index
                  
                if tagVerts[linkVert]['group'] != NumGroup: 
                    nLinked += 1
                    
                    if tagVerts[linkVert]['group'] == -1:
                        nextInternal = linkVert
            
            print ("nextInternal: " + str(nextInternal))
            if (g + nLinked + 1 <= 12):
                tagVerts[currentIndex]['group'] = NumGroup
                tagVerts[currentIndex]['read'] = True
            
                internalNodes.append(currentIndex)
                g += 1
                g = g + nLinked - 1
                if nextInternal == -1:
                    print("Failed LOL by " + str(currentIndex))
                    #Add search again? 
                    #if g < 12 search from a list
                    #TEST CODE
                    
                    #END TEST CODE
                    break
                else:
                    currentIndex = nextInternal
            else:
                break
                
                
        #make sure list is unique
        assert len(internalNodes) == len(set(internalNodes))
        
        groupNodes = []
        for i in range(len(internalNodes)):
            groupNodes.append({})
            
            groupNodes[i]['realIndex'] = internalNodes[i]
            groupNodes[i]['x'] = bm.verts[internalNodes[i]].co.x
            groupNodes[i]['y'] = bm.verts[internalNodes[i]].co.y
            groupNodes[i]['z'] = bm.verts[internalNodes[i]].co.z
            groupNodes[i]['type'] = 2
            groupNodes[i]['next'] = -1
          
        for i in range(len(internalNodes)):
            for link in bm.verts[internalNodes[i]].link_edges:
                
                linkVert = link.verts[0].index
                if linkVert == internalNodes[i]:
                    linkVert = link.verts[1].index
                    
                if tagVerts[linkVert]['group'] != NumGroup:
                    #externalNodes
                    externalNode = {}
                    externalNode['realIndex'] = linkVert
                    externalNode['x'] = (bm.verts[linkVert].co.x + bm.verts[internalNodes[i]].co.x)/2
                    externalNode['y'] = (bm.verts[linkVert].co.y + bm.verts[internalNodes[i]].co.y)/2
                    externalNode['z'] = (bm.verts[linkVert].co.z + bm.verts[internalNodes[i]].co.z)/2
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
            ignoredNode['x'] = 0
            ignoredNode['y'] = 0
            ignoredNode['z'] = 0
            groupNodes.append(ignoredNode)
            
        file.write("0, -1\n")
        #write relation
        for node in groupNodes:
            file.write( "\t{}, {}, {}, {:.2f}, {:.2f}, {:.2f}, {}, {}, {}, {}, {}, {}\n".format(
                node['type'], 
                node['next'], 
                0,
                node['x'] * 16,
                node['y'] * 16,
                node['z'] * 16,
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

    
def exportVehiclePaths(filepath, ob):
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
        tagEdges[i]['type'] = "none" # internal/external
        
    for v in bm.verts:
        if tagVerts[v.index]['read']:
            continue
            
        currentIndex = v.index
        internalNodes = []
        g = 0
        while True:
            assert len(bm.verts[currentIndex].link_edges) > 0
            
            nextInternal = -1
            nLinked = 0
            for link in bm.verts[currentIndex].link_edges:
                
                linkVert = link.verts[0].index
                if linkVert == currentIndex:
                    linkVert = link.verts[1].index
                  
                if tagVerts[linkVert]['group'] != NumGroup: 
                    nLinked += 1
                    
                    if tagVerts[linkVert]['group'] == -1:
                        nextInternal = linkVert
            
            print ("nextInternal: " + str(nextInternal))
            if (g + nLinked + 1 <= 12):
                tagVerts[currentIndex]['group'] = NumGroup
                tagVerts[currentIndex]['read'] = True
            
                internalNodes.append(currentIndex)
                g += 1
                g = g + nLinked - 1
                if nextInternal == -1:
                    print("Failed LOL by " + str(currentIndex))
                    #Add search again? 
                    #if g < 12 search from a list
                    #TEST CODE
                    
                    #END TEST CODE
                    break
                else:
                    currentIndex = nextInternal
            else:
                break
                
                
        #make sure list is unique
        assert len(internalNodes) == len(set(internalNodes))
        
        groupNodes = []
        for i in range(len(internalNodes)):
            groupNodes.append({})
            
            groupNodes[i]['realIndex'] = internalNodes[i]
            groupNodes[i]['x'] = bm.verts[internalNodes[i]].co.x
            groupNodes[i]['y'] = bm.verts[internalNodes[i]].co.y
            groupNodes[i]['z'] = bm.verts[internalNodes[i]].co.z
            groupNodes[i]['type'] = 2
            groupNodes[i]['next'] = -1
          
        for i in range(len(internalNodes)):
            for link in bm.verts[internalNodes[i]].link_edges:
                
                linkVert = link.verts[0].index
                if linkVert == internalNodes[i]:
                    linkVert = link.verts[1].index
                    
                if tagVerts[linkVert]['group'] != NumGroup:
                    #externalNodes
                    externalNode = {}
                    externalNode['realIndex'] = linkVert
                    externalNode['x'] = (bm.verts[linkVert].co.x + bm.verts[internalNodes[i]].co.x)/2
                    externalNode['y'] = (bm.verts[linkVert].co.y + bm.verts[internalNodes[i]].co.y)/2
                    externalNode['z'] = (bm.verts[linkVert].co.z + bm.verts[internalNodes[i]].co.z)/2
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
            ignoredNode['x'] = 0
            ignoredNode['y'] = 0
            ignoredNode['z'] = 0
            groupNodes.append(ignoredNode)
            
        file.write("0, -1\n")
        #write relation
        for node in groupNodes:
            file.write( "\t{}, {}, {}, {:.2f}, {:.2f}, {:.2f}, {}, {}, {}, {}, {}, {}\n".format(
                node['type'], 
                node['next'], 
                0,
                node['x'] * 16,
                node['y'] * 16,
                node['z'] * 16,
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
