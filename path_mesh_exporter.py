import bpy
import bmesh
from mathutils import Vector

from .ui_constants import *
    
def exportPaths(filepath, ob):
    print("Exporting to: " + filepath)
    print("Exporting Object: " + ob.name)
    file = open(filepath, 'w')
    
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
                  
                if tagVerts[linkVert]['group'] == -1:
                    nextInternal = linkVert
                    nLinked += 1
                else:
                    print("Loop Detected at: " + str(linkVert))
            
            
            print ("nLinked: " + str(nLinked))
            print ("nextInternal: " + str(nextInternal))
            if (g + nLinked + 1 <= 12):
                tagVerts[currentIndex]['group'] = NumGroup
                tagVerts[currentIndex]['read'] = True
            
                internalNodes.append(currentIndex)
                g += 1
                g = g + nLinked - 1
                print (g)
                if nextInternal == -1:
                    print("Failed LOL by " + str(currentIndex))
                    break
                else:
                    currentIndex = nextInternal
            else:
                break
                
        
        #TEST CODE
        print("""
import bpy
import bmesh
#get attribute
obj = bpy.context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)

selectedEdge = [e for e in bm.edges if e.select]
selectedVert = [v for v in bm.verts if v.select]
        """
        )
        for x in internalNodes:
            print("bm.verts[" + str(x) + "].select = True")
        break
        print("")
        #END TEST CODE
        NumGroup += 1
                    
    bm.to_mesh(me)
    bm.free()
    file.close()
