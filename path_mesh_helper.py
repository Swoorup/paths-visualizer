import bpy
import bmesh
from mathutils import Vector

from . import sapaths
from .ui_constants import *

def debugprintNode(msg, node):
    print('\n' + msg)

    print('area id:' + str(node[NODE_AREAID]))
    print('area id:' + str(node[NODE_ID]))
    print('x: ' + str(node['x']))
    print('y: ' + str(node['y']))
    print('z: ' + str(node['z']))

    print('\n')

def AddPathMeshVertLayers(bm):
    bm.verts.layers.float.new(NODE_WIDTH)
    bm.verts.layers.int.new(NODE_BAHAVIOUR)
    bm.verts.layers.int.new(NODE_ISDEADEND)
    bm.verts.layers.int.new(NODE_ISIGNORED)
    bm.verts.layers.int.new(NODE_ISROADBLOCK)
    bm.verts.layers.int.new(NODE_ISEMERGENCYVEHICLEONLY)
    bm.verts.layers.int.new(NODE_ISRESTRICTEDACCESS)
    bm.verts.layers.int.new(NODE_ISDONTWANDER)
    bm.verts.layers.int.new(NODE_SPEEDLIMIT)
    bm.verts.layers.int.new(NODE_SPAWNPROBABILITY)
    bm.verts.layers.int.new(NODE_NUMLEFTLANES)
    bm.verts.layers.int.new(NODE_NUMRIGHTLANES)
    bm.verts.layers.int.new(NODE_ISTRAINCROSSING)
    bm.verts.layers.string.new(NODE_TYPE)
    bm.verts.layers.int.new(NODE_AREAID)
    bm.verts.layers.int.new(NODE_ID)
    bm.verts.layers.int.new(NODE_FLOOD)
    bm.verts.layers.int.new(NODE_TRAFFICLIGHTDIRECTION)
    bm.verts.layers.int.new(NODE_TRAFFICLIGHTBEHAVIOUR)

def CopyValuesFromNodeToBMVert(node, bm, bmvert, nodeType, carPathLink=None):
    bmvert[bm.verts.layers.float[NODE_WIDTH]]                = node[NODE_WIDTH]
    bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]              = node[NODE_BAHAVIOUR]
    bmvert[bm.verts.layers.int[NODE_ISDEADEND]]              = node[NODE_ISDEADEND]
    bmvert[bm.verts.layers.int[NODE_ISIGNORED]]              = node[NODE_ISIGNORED]
    bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]]            = node[NODE_ISROADBLOCK]
    bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] = node[NODE_ISEMERGENCYVEHICLEONLY]
    bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]]     = node[NODE_ISRESTRICTEDACCESS]
    bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]]           = node[NODE_ISDONTWANDER]
    bmvert[bm.verts.layers.int[NODE_SPEEDLIMIT]]             = node[NODE_SPEEDLIMIT]
    bmvert[bm.verts.layers.int[NODE_SPAWNPROBABILITY]]       = node[NODE_SPAWNPROBABILITY]
    bmvert[bm.verts.layers.string[NODE_TYPE]]                = str.encode(nodeType)
    bmvert[bm.verts.layers.int[NODE_AREAID]]                 = node[NODE_AREAID]
    bmvert[bm.verts.layers.int[NODE_ID]]                     = node[NODE_ID]
    bmvert[bm.verts.layers.int[NODE_FLOOD]]                  = node[NODE_FLOOD]

    if carPathLink == None:
        bmvert[bm.verts.layers.int[NODE_NUMLEFTLANES]]           = 0
        bmvert[bm.verts.layers.int[NODE_NUMRIGHTLANES]]          = 0
        bmvert[bm.verts.layers.int[NODE_ISTRAINCROSSING]]        = 0
        bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTDIRECTION]]  = 0
        bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTBEHAVIOUR]]  = 0
    else:
        bmvert[bm.verts.layers.int[NODE_NUMLEFTLANES]]           = carPathLink[NODE_NUMLEFTLANES]
        bmvert[bm.verts.layers.int[NODE_NUMRIGHTLANES]]          = carPathLink[NODE_NUMRIGHTLANES]
        bmvert[bm.verts.layers.int[NODE_ISTRAINCROSSING]]        = carPathLink[NODE_ISTRAINCROSSING]
        bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTDIRECTION]]  = carPathLink[NODE_TRAFFICLIGHTDIRECTION]
        bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTBEHAVIOUR]]  = carPathLink[NODE_TRAFFICLIGHTBEHAVIOUR]

def createVehicleMesh(nodes):
    verts = []
    edges = []

""" TODO: have edge layer to hold lane and other links information
    Its quite evident this information can't be stored per vertex
"""

def loadVehicleMesh(ob, nodes):
    bm = bmesh.new()
    bm.from_mesh(ob.data)

    # add the properties
    AddPathMeshVertLayers(bm)
    
    # add all vertices
    for node in nodes:
        bmvert = bm.verts.new((node['x'], node['y'], node['z']))
        CopyValuesFromNodeToBMVert(node, bm, bmvert, 'path')

    # add carpathlink vertex usually in the middle
    for node in nodes:
        for link in node['_links']:
            linkedNode = link['targetNode']
            linkedIndex = linkedNode['id']
            carpathlink = link['carpathlink']
            
            # carpathlinks point from higher id to lower id
            if node['id'] > linkedNode['id']:
                bmvert = bm.verts.new((carpathlink['x'], carpathlink['y'], (node['z'] + linkedNode['z']) / 2.0))
                CopyValuesFromNodeToBMVert(node, bm, bmvert, 'link', carpathlink)

    bm.verts.index_update()
    bm.verts.ensure_lookup_table()

    # connect all the edge data
    k = len(nodes) # offset of carpathlink data
    for node in nodes:
        i = node['id']
        for link in node['_links']:
            linkedNode = link['targetNode']
            linkedIndex = linkedNode['id']
            carpathlink = link['carpathlink']
            
            # carpathlinks point from higher id to lower id
            if node['id'] > linkedNode['id']:
                # from and to order needs to be preserved to hold lane information, make sure blender does not play around with these
                # TODO: check if link order is preserved by blender
                # link to carpathpath 
                bm.edges.new( (bm.verts[i], bm.verts[k]))
                # then to targetnode
                bm.edges.new( (bm.verts[k], bm.verts[linkedIndex])) 
                # copy the carpathlink information
                k = k+1


    #bm.edges.ensure_lookup_table()
    #bm.verts.ensure_lookup_table()
    
    bm.to_mesh(ob.data)
    bm.free()

def loadCarPathLinkMesh(ob, pathlinks):
    bm = bmesh.new()
    bm.from_mesh(ob.data)

    for carpathlink in pathlinks:
        bm.verts.new((carpathlink['x'], carpathlink['y'], 0.0))
        bm.verts.new((carpathlink['x'] + carpathlink['dirX'] , carpathlink['y'] + carpathlink['dirY'], 0.0))
        bm.verts.new((carpathlink['navigationTarget']['x'] , carpathlink['navigationTarget']['y'], 0.0))
    
        bm.verts.index_update()
    bm.verts.ensure_lookup_table()

    for carpathlink in pathlinks:
        id = carpathlink['id']
        bm.edges.new((bm.verts[id * 3], bm.verts[id * 3 + 1]))
        bm.edges.new((bm.verts[id * 3], bm.verts[id * 3 + 2]))
    bm.to_mesh(ob.data)
    bm.free()

    
def loadPedPathMesh(ob, nodes):
    bm = bmesh.new()
    bm.from_mesh(ob.data)

    # add all vertices
    for node in nodes:
        bm.verts.new((node['x'], node['y'], node['z']))

    bm.verts.index_update()
    bm.verts.ensure_lookup_table()

    # connect all the edge data
    for node in nodes:
        i = node['id']
        for link in node['_links']:
            linkedNode = link['targetNode']
            linkedIndex = linkedNode['id']
            
            try:
                bm.edges.new((bm.verts[i], bm.verts[linkedIndex]))
            except ValueError: # already exist
                continue

    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()

    node_width_key = bm.verts.layers.float.new('node_width')
    node_area_id = bm.verts.layers.int.new('node_areaid')
    node_node_id = bm.verts.layers.int.new('node_id')
    node_behaviour = bm.verts.layers.int.new('node_behaviour')
    # add the per node properties
    for node in nodes:
        bm.verts[node['id']][node_width_key] = node['width']
        bm.verts[node['id']][node_area_id] = node['areaID']
        bm.verts[node['id']][node_node_id] = node['nodeID']
        bm.verts[node['id']][node_behaviour] = node['behaviourType']

    bm.to_mesh(ob.data)
    bm.free()

def loadSAPathsAsMesh(nodesDir):
    paths = sapaths.SAPaths()
    paths.load_nodes_from_directory(nodesDir)    

    # Create mesh 
    me = bpy.data.meshes.new('myMesh') 
    # Create object
    ob = bpy.data.objects.new('PathMeshCars', me) 
    bpy.context.scene.objects.link(ob)
    loadVehicleMesh(ob, paths.carnodes)

    # Create object
    ob = bpy.data.objects.new('PathMeshBoats', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadVehicleMesh(ob, paths.boatnodes)

    # Create object
    ob = bpy.data.objects.new('PathMeshPed', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    #loadPedPathMesh(ob, paths.pednodes)

    #DEBUG HELPER
    ob = bpy.data.objects.new('boatpathlinknodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadCarPathLinkMesh(ob, paths.boatpathlinknodes)
    ob = bpy.data.objects.new('carpathlinknodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    #loadCarPathLinkMesh(ob, paths.carpathlinknodes)
    