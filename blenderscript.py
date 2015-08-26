__author__ = 'Swoorup'
import sapaths
import bpy
from mathutils import Vector

paths = sapaths.SAPaths()
paths.load_nodes_from_directory(r"E:\Output")


theLineData = bpy.data.curves.new(name="sasas",type='CURVE')
theLineData.dimensions = '3D'
theLineData.fill_mode = 'FULL'



for i in range(len(paths.nodes)):
    # Traverse through the car path nodes for tracing a line
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
            if nodeID >  carpathlink['targetID']:
                points.append((linkNode['x'], linkNode['y'], linkNode['z']))
                ID = link['targetID']

    out2 = []
    [out2.extend(list(i)+[0.0]) for i in points]
    # define points that make the line
    polyline = theLineData.splines.new('POLY')
    polyline.points.add(len(points) - 1)
    polyline.points.foreach_set('co', out2)

    # create an object that uses the linedata
    theLine = bpy.data.objects.new('LineOne',theLineData)
    bpy.context.scene.objects.link(theLine)
    theLine.location = (0.0,0.0,0.0)