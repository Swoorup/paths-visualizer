import bpy
import bmesh
from mathutils import Vector

from .gta import sapaths, ivpaths
from .ui_constants import *
from .mesh_layer import AddPathMeshLayers

def debugprintNode(msg, node):
    print('\n' + msg)

    print('area id:' + str(node[NODE_AREAID]))
    print('area id:' + str(node[NODE_ID]))
    print('x: ' + str(node['x']))
    print('y: ' + str(node['y']))
    print('z: ' + str(node['z']))

    print('\n')

def CopyAttributesFromNodeToBMVert(node, bm, bmvert, nodeType):
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

def CopyAttributesFromLinkToBMEdge(carPathLink, bm, bmedge):
    bmedge[bm.edges.layers.float[EDGE_WIDTH]]                = carPathLink[EDGE_WIDTH]
    bmedge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]           = carPathLink[EDGE_NUMLEFTLANES]
    bmedge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]          = carPathLink[EDGE_NUMRIGHTLANES]
    bmedge[bm.edges.layers.int[EDGE_ISTRAINCROSSING]]        = carPathLink[EDGE_ISTRAINCROSSING]
    bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]]  = carPathLink[EDGE_TRAFFICLIGHTDIRECTION]
    bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]]  = carPathLink[EDGE_TRAFFICLIGHTBEHAVIOUR]

        
def loadVehicleMesh(ob, nodes):
    bm = bmesh.new()
    bm.from_mesh(ob.data)

    # add the properties
    AddPathMeshLayers(bm)
    
    # add all vertices
    for node in nodes:
        bmvert = bm.verts.new((node['x'], node['y'], node['z']))
        CopyAttributesFromNodeToBMVert(node, bm, bmvert, 'node')

    # add carpathlink vertex usually in the middle
    for node in nodes:
        for link in node['_links']:
            linkedNode = link['targetNode']
            linkedIndex = linkedNode['id']
            carpathlink = link['carpathlink']
            
            # carpathlinks point from higher id to lower id
            if node['id'] > linkedNode['id']:
                bmvert = bm.verts.new((carpathlink['x'], carpathlink['y'], (node['z'] + linkedNode['z']) / 2.0))
                CopyAttributesFromNodeToBMVert(node, bm, bmvert, 'link')

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
                bmedge = bm.edges.new( (bm.verts[i], bm.verts[k]))
                CopyAttributesFromLinkToBMEdge(carpathlink, bm, bmedge)
                # then to targetnode
                bmedge = bm.edges.new( (bm.verts[k], bm.verts[linkedIndex])) 
                CopyAttributesFromLinkToBMEdge(carpathlink, bm, bmedge)
                # copy the carpathlink information
                k = k+1
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
    loadPedPathMesh(ob, paths.pednodes)
    
def exportPaths(context):
    pass

def loadivVehicleMesh(ob, nodes):
    bm = bmesh.new()
    bm.from_mesh(ob.data)

    # add the properties
    AddPathMeshLayers(bm)
    
    # add all vertices
    for node in nodes:
        bmvert = bm.verts.new((node['x'], node['y'], node['z']))
        CopyAttributesFromNodeToBMVert(node, bm, bmvert, 'node')

    bm.verts.index_update()
    bm.verts.ensure_lookup_table()

    # connect all the edge data
    k = len(nodes) # offset of carpathlink data
    for node in nodes:
        i = node['id']
        for link in node['_links']:
            linkedNode = link['targetNode']
            linkedIndex = linkedNode['id']

            try:
                bmedge = bm.edges.new( (bm.verts[i], bm.verts[linkedIndex]))
                #CopyAttributesFromLinkToBMEdge(carpathlink, bm, bmedge)
            except ValueError: # already exist
                continue

    bm.to_mesh(ob.data)
    bm.free()

def loadIVPathsAsMesh(nodesDir):
    paths = ivpaths.IVPaths()
    paths.load_nodes_from_directory(nodesDir)    

    # Create mesh 
    me = bpy.data.meshes.new('myMesh') 
    # Create object
    ob = bpy.data.objects.new('PathMeshCars', me) 
    bpy.context.scene.objects.link(ob)
    loadivVehicleMesh(ob, paths.carnodes)

    # Create object
    ob = bpy.data.objects.new('PathMeshBoats', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadivVehicleMesh(ob, paths.boatnodes)