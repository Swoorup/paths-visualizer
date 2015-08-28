__author__ = 'Swoorup'
import sapaths
import bpy
from mathutils import Vector

import imp
imp.reload(sapaths)

paths = sapaths.SAPaths()
paths.load_nodes_from_directory(r"G:\paths-visualizer\Vanilla\Compiled\SA")



#"""
def addPointsToCurve(node, pointList):
    if node['_btraversed'] == True:
        return False

    pointList.append((node['x'], node['y'], node['z']))
    node['_btraversed'] = True
    return True

def tracePathCurve(nodestart):
    points = []
    addPointsToCurve(nodestart, points)

    # select the link which is actually a line
    secondNode = None
    for link in nodestart['_links']:
        linkedNode = link['targetNode']
        if linkedNode['_btraversed']:
            continue
        nSubLink = len(linkedNode['_links'])
        if nSubLink == 2 or nSubLink == 1:
            secondNode = linkedNode
            break

    if secondNode == None:
        return

    #assert(secondNode['_btraversed'] != True)
    addPointsToCurve(secondNode, points)

    node = secondNode
    while True:
        #if len(node['_links']) != 2:
            #break

        oldnode = node
        for link in node['_links']:
            linkedNode = link['targetNode']
            if addPointsToCurve(linkedNode, points) == False:
                continue

            node = linkedNode
            break
        
        if oldnode is node:
            break

    endnode = node
    addPointsToCurve(endnode, points)

    out2 = []
    [out2.extend(list(j)+[0.0]) for j in points]

    theLineData = bpy.data.curves.new(name="sasas",type='CURVE')
    theLineData.dimensions = '3D'
    theLineData.fill_mode = 'FULL'

    # define points that make the line
    polyline = theLineData.splines.new('POLY')
    polyline.points.add(len(points) - 1)
    polyline.points.foreach_set('co', out2)

    theLine = bpy.data.objects.new('LineOne',theLineData)
    bpy.context.scene.objects.link(theLine)
    theLine.location = (0.0,0.0,0.0)

for node in paths.carnodes:
    if node['_btraversed']:
        continue

    # always trace line from a junction
    #if len(node['_links']) != 2:
    tracePathCurve(node)


# create an object that uses the linedata


"""
for i in paths.carnodes:
    if i['_btraversed']:
        continue

    # start a line from an intersection
    #if len(paths.nodes[i]['_links']) == 2:
        #continue

    # Traverse through the car path nodes for tracing a line
    #print(i, paths.nodes[i]['floodcolor'])
    points = []
    node = i
    while (True):
        if node['_btraversed']:
            break

        # A line can have only 2 endpoints
        if len(node['_links']) > 2:
            break

        points.append((node['x'], node['y'], node['z']))
        node['_btraversed'] = True

        for link in node['_links']:
            linkNode = link['targetNode']
            carpathlink = link['carpathlink']
            if node is not carpathlink['navigationTarget']:
                points.append((linkNode['x'], linkNode['y'], linkNode['z']))
                node = link['targetNode']

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

# """