__author__ = 'Swoorup'
import sapaths
import bpy
import bmesh
from mathutils import Vector

import imp
imp.reload(sapaths)

def loadPathMesh(ob, nodes):
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

def loadSAPathsAsMesh(nodesDir):
    paths = sapaths.SAPaths()
    paths.load_nodes_from_directory(nodesDir)    
    #paths.load_nodes_from_directory(r"E:\Output")  

    # Create mesh 
    me = bpy.data.meshes.new('myMesh') 
    # Create object
    ob = bpy.data.objects.new('carNodes', me) 
    bpy.context.scene.objects.link(ob)
    loadPathMesh(ob, paths.carnodes)

    # Create object
    ob = bpy.data.objects.new('boatNodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadPathMesh(ob, paths.boatnodes)

    # Create object
    ob = bpy.data.objects.new('pedNodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    #loadPathMesh(ob, paths.pednodes)

    #DEBUG HELPER
    ob = bpy.data.objects.new('boatpathlinknodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadCarPathLinkMesh(ob, paths.boatpathlinknodes)
    ob = bpy.data.objects.new('carpathlinknodes', bpy.data.meshes.new('myMesh')) 
    bpy.context.scene.objects.link(ob)
    loadCarPathLinkMesh(ob, paths.carpathlinknodes)
    