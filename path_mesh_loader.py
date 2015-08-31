import bpy
import bmesh
from mathutils import Vector

from . import sapaths
from .ui_constants import *

def AddPathMeshVertLayers(bm):
    bm.verts.layers.float(NODE_WIDTH)
    bm.verts.layers.int(NODE_BAHAVIOUR)
    bm.verts.layers.int(NODE_ISDEADEND)
    bm.verts.layers.int(NODE_ISIGNORED)
    bm.verts.layers.int(NODE_ISROADBLOCK)
    bm.verts.layers.int(NODE_ISEMERGENCYVEHICLEONLY)
    bm.verts.layers.int(NODE_ISRESTRICTEDACCESS)
    bm.verts.layers.int(NODE_ISDONTWANDER)
    bm.verts.layers.int(NODE_SPEEDLIMIT)
    bm.verts.layers.int(NODE_SPAWNPROBABILITY)
    bm.verts.layers.int(NODE_NUMLEFTLANES)
    bm.verts.layers.int(NODE_NUMRIGHTLANES)
    bm.verts.layers.int(NODE_ISTRAINCROSSING)
    bm.verts.layers.string(NODE_TYPE)
    bm.verts.layers.int(NODE_AREAID)
    bm.verts.layers.int(NODE_ID)
    bm.verts.layers.int(NODE_FLOOD)
    bm.verts.layers.int(NODE_TRAFFICLIGHTDIRECTION)
    bm.verts.layers.int(NODE_TRAFFICLIGHTBEHAVIOUR)

def CopyValuesFromNodeToBMVert(node, bm, bmvert, nodeType):
    bmvert[bm.verts.layers.float[NODE_WIDTH]]                  = node[NODE_WIDTH]
    bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]              = node[NODE_BAHAVIOUR]
    bmvert[bm.verts.layers.int[NODE_ISDEADEND]]              = node[NODE_ISDEADEND]
    bmvert[bm.verts.layers.int[NODE_ISIGNORED]]              = node[NODE_ISIGNORED]
    bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]]            = node[NODE_ISROADBLOCK]
    bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] = node[NODE_ISEMERGENCYVEHICLEONLY]
    bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]]     = node[NODE_ISRESTRICTEDACCESS]
    bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]]           = node[NODE_ISDONTWANDER]
    bmvert[bm.verts.layers.int[NODE_SPEEDLIMIT]]             = node[NODE_SPEEDLIMIT]
    bmvert[bm.verts.layers.int[NODE_SPAWNPROBABILITY]]       = node[NODE_SPAWNPROBABILITY]
    bmvert[bm.verts.layers.int[NODE_NUMLEFTLANES]]           = node[NODE_NUMLEFTLANES]
    bmvert[bm.verts.layers.int[NODE_NUMRIGHTLANES]]          = node[NODE_NUMRIGHTLANES]
    bmvert[bm.verts.layers.int[NODE_ISTRAINCROSSING]]        = node[NODE_ISTRAINCROSSING]
    bmvert[bm.verts.layers.string[NODE_TYPE]]                   = nodeType
    bmvert[bm.verts.layers.int[NODE_AREAID]]                 = node[NODE_AREAID]
    bmvert[bm.verts.layers.int[NODE_ID]]                     = node[NODE_ID]
    bmvert[bm.verts.layers.int[NODE_FLOOD]]                  = node[NODE_FLOOD]
    bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTDIRECTION]]  = node[NODE_TRAFFICLIGHTDIRECTION]
    bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTBEHAVIOUR]]  = node[NODE_TRAFFICLIGHTBEHAVIOUR]

def loadVehicleMesh(ob, nodes):
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
            carpathlink = link['carpathlink']
            linkedIndex = linkedNode['id']
            
            try:
                #bm.edges.new((bm.verts[i], bm.verts[carpathlink['navigationTarget']['id']]))
                bm.edges.new((bm.verts[i], bm.verts[linkedIndex]))
            except ValueError: # already exist
                continue

    bm.edges.ensure_lookup_table()
    bm.verts.ensure_lookup_table()
    
    AddPathMeshVertLayers(bm)
    # add the per node properties
    for node in nodes:
        CopyValuesFromNodeToBMVert(node, bm, bm.verts[node['id']], 'path')

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
    loadPedPathMesh(ob, paths.carnodes)

    # Create object
    ob = bpy.data.objects.new('PathMeshBoats', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadPedPathMesh(ob, paths.boatnodes)

    # Create object
    ob = bpy.data.objects.new('PathMeshPed', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadPedPathMesh(ob, paths.pednodes)

    #DEBUG HELPER
    ob = bpy.data.objects.new('boatpathlinknodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadCarPathLinkMesh(ob, paths.boatpathlinknodes)
    ob = bpy.data.objects.new('carpathlinknodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadCarPathLinkMesh(ob, paths.carpathlinknodes)
    