__author__ = 'Swoorup'
import sapaths
import bpy
from mathutils import Vector

import imp
imp.reload(sapaths)

paths = sapaths.SAPaths()
paths.load_nodes_from_directory(r"F:\paths-visualizer\Vanilla\Compiled\SA")

theLineData = bpy.data.curves.new(name="sasas",type='CURVE')
theLineData.dimensions = '3D'
theLineData.fill_mode = 'FULL'
    
for i in range(len(paths.nodes)):
    if paths.nodes[i]['_nodeType'] == 'ped':# or paths.nodes[i]['isWaterNode']:
        continue

    if paths.nodes[i]['_btraversed']:
        continue
        
    # start a line from an intersection
    if len(paths.nodes[i]['_links']) == 2:
        continue

    # Traverse through the car path nodes for tracing a line
    #print(i, paths.nodes[i]['floodcolor'])
    nodeID = i
    points = []
    while (True):
        node = paths.nodes[nodeID]

        if node['_btraversed']:
            break

        # A line can have only 2 endpoints
        if len(node['_links']) > 2:
            break

        points.append((node['x'], node['y'], node['z']))
        node['_btraversed'] = True

        for link in node['_links']:
            linkNode = paths.nodes[link['targetID']]
            carpathlink = paths.carpathlinks[link['carpathlinkID']]
            if nodeID > carpathlink['targetID']:
                points.append((linkNode['x'], linkNode['y'], linkNode['z']))
                nodeID = link['targetID']

    out2 = []
    [out2.extend(list(j)+[0.0]) for j in points]
    # define points that make the line
    polyline = theLineData.splines.new('POLY')
    polyline.points.add(len(points) - 1)
    polyline.points.foreach_set('co', out2)

# create an object that uses the linedata
theLine = bpy.data.objects.new('LineOne',theLineData)
bpy.context.scene.objects.link(theLine)
theLine.location = (0.0,0.0,0.0)

# blender is slow as hell in editing huge large amount of curves even in a single object
#bpy.ops.object.convert(target='MESH')