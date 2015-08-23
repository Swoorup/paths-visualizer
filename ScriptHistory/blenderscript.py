import math
import bpy
import bmesh
import itertools
import mathutils
import sys
import os

from struct import unpack
from io import BytesIO

print("Path: " + os.path.dirname(os.path.realpath(__file__)))
print(bpy.data.filepath)
sys.path.append(r".\\")
sys.path.append(r"..\\")

for i in sys.path: print(i)
from sapaths import SAPath


MAX_SEGMENT = 8
BLOCK_SIZE = 750.0


class SAPath():
	def __init__(self, node):
		self.path = BytesIO(open(node, "rb").read())
		self.header = {}
		self.pathnodes = []
		self.navinodes = []
		self.links = []
		self.navilinks = []
		self.linklengths = []
		self._offset = 20
		
		# headers
		self.header['nodes']	 = unpack('I', self.path.read(4))[0]
		self.header['vehnodes']	 = unpack('I', self.path.read(4))[0]
		self.header['pednodes']	 = unpack('I', self.path.read(4))[0]
		self.header['navinodes'] = unpack('I', self.path.read(4))[0]
		self.header['links']	 = unpack('I', self.path.read(4))[0]
			
	def Headers(self):
		return self.header
	
	def Paths(self):
		if len(self.pathnodes) != self.header['nodes']:
			self.path.seek(self._offset, 0)
			for i in range(self.header['nodes']):
				self.pathnodes.append({})
				self.pathnodes[i]['mem']	 = unpack('I', self.path.read(4))[0]
				self.pathnodes[i]['zero']	 = unpack('I', self.path.read(4))[0]
				self.pathnodes[i]['x']		 = float(unpack('h', self.path.read(2))[0]) / 8
				self.pathnodes[i]['y']		 = float(unpack('h', self.path.read(2))[0]) / 8
				self.pathnodes[i]['z']		 = float(unpack('h', self.path.read(2))[0]) / 8
				self.pathnodes[i]['heuristic'] = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['baseLink']	 = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['area']	 = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['node']	 = unpack('h', self.path.read(2))[0]
				self.pathnodes[i]['width']	 = unpack('b', self.path.read(1))[0] / 8
				self.pathnodes[i]['type']	 = unpack('b', self.path.read(1))[0]
				self.pathnodes[i]['flags']	 = unpack('I', self.path.read(4))[0]
		return self.pathnodes
			
	def NaviNodes(self):
		if len(self.navinodes) != self.header['navinodes']:
			self.path.seek(self._offset + (self.header['nodes'] * 28), 0)
			for i in range(self.header['navinodes']):
				self.navinodes.append({})
				self.navinodes[i]['x']		= float(unpack('h', self.path.read(2))[0]) / 8
				self.navinodes[i]['y']		= float(unpack('h', self.path.read(2))[0]) / 8
				self.navinodes[i]['area']	= unpack('h', self.path.read(2))[0]
				self.navinodes[i]['node']	= unpack('h', self.path.read(2))[0]
				self.navinodes[i]['disx']	= float(unpack('b', self.path.read(1))[0]) / 8
				self.navinodes[i]['disy']	= float(unpack('b', self.path.read(1))[0]) / 8
				self.navinodes[i]['flags']	= unpack('I', self.path.read(4))[0]
		return self.navinodes
		
	def Links(self):
		if len(self.links) != self.header['links']:
			self.path.seek(self._offset + (self.header['nodes'] * 28) + (self.header['navinodes'] * 14), 0)
			for i in range(self.header['links']):
				self.links.append({})
				self.links[i]['area']	= unpack('h', self.path.read(2))[0]
				self.links[i]['node']	= unpack('h', self.path.read(2))[0]
		return self.links
		
	def NaviLinks(self):
		if len(self.navilinks) != self.header['links']:
			self.path.seek(self._offset + (self.header['nodes'] * 28) + (self.header['navinodes'] * 14) + (self.header['links'] * 4) + 768, 0)
			for i in range(self.header['links']):
				self.navilinks.append(unpack('h', self.path.read(2))[0])
		return self.navilinks
	
	def LinkLengths(self):
		if len(self.linklengths) != self.header['links']:
			self.path.seek(self._offset + (self.header['nodes'] * 28) + (self.header['navinodes'] * 14) + (self.header['links'] * 4) + 768 + (self.header['links'] * 2), 0)
			for	i in range(self.header['links']):
				self.linklengths.append(unpack('b', self.path.read(1))[0])
		return self.linklengths
		
	def Close(self):
		 self.path.close()
		 

def createLine(lineName, pointList, thickness):
    # setup basic line data
    theLineData = bpy.data.curves.new(name=lineName,type='CURVE')
    theLineData.dimensions = '3D'
    theLineData.fill_mode = 'FULL'
    theLineData.bevel_depth = thickness
    # define points that make the line
    polyline = theLineData.splines.new('POLY')
    polyline.points.add(len(pointList)-1)
    for idx in range(len(pointList)):
        polyline.points[idx].co = (pointList[idx])+(1.0,)

    # create an object that uses the linedata
    theLine = bpy.data.objects.new('LineOne',theLineData)
    bpy.context.scene.objects.link(theLine)
    theLine.location = (0.0,0.0,0.0)

    # setup a material
    lmat = bpy.data.materials.new('Linematerial')
    lmat.diffuse_color = (0.0,0.0,1.0)
    lmat.use_shadeless = True
    theLine.data.materials.append(lmat)
	
class SAPathVisualizer(bpy.types.Operator) :
	bl_idname = "mesh.makepaths"
	bl_label = "Make paths"
	
	def __init__(self):
		self.pathfiles = []
	
	def RenderNaviNodesLines(self, context):
	
		inboundline = []
		for i in self.pathfiles:
			for j in i.NaviNodes():
				# Link object to scene
				inboundline.append((j['x'], j['y'], 0.0))
		
		createLine('LineOne', inboundline, 0.05)
				
	def RenderNaviNodesBMesh(self, context):
		for i in self.pathfiles:
			for j in i.NaviNodes():
				
				me = bpy.data.meshes.new('myMesh') 
				ob = bpy.data.objects.new('myObject', me)   
					
				
				# Get a BMesh representation
				bm = bmesh.new()   # create an empty BMesh
				bm.from_mesh(me)   # fill it in from a Mesh
				
				# Hot to create vertices
				vertex1 = bm.verts.new( (0.0, 0.0, 3.0) )
				vertex2 = bm.verts.new( (2.0, 0.0, 3.0) )
				vertex3 = bm.verts.new( (2.0, 2.0, 3.0) )
				vertex4 = bm.verts.new( (0.0, 2.0, 3.0) )
				
				# Initialize the index values of this sequence.
				bm.verts.index_update()
				
				# How to create edges    
				bm.edges.new( (vertex1, vertex2) )
				bm.edges.new( (vertex2, vertex3) )
				bm.edges.new( (vertex3, vertex4) )
				bm.edges.new( (vertex4, vertex1) )
				
				# How to create a face
				# it's not necessary to create the edges before, I made it only to show how create 
				# edges too
				#bm.faces.new( (vertex1, vertex2, vertex3, vertex4) )
				
				# Finish up, write the bmesh back to the mesh
				bm.to_mesh(me)
				
				# Link object to scene
				ob.location = (j['x'], j['y'], 0.0)
				bpy.context.scene.objects.link(ob)

		
	def RenderNaviNodes(self, context):
		Vertices = []
		for i in self.pathfiles:
			for j in i.NaviNodes():
				Vertices.append((j['x'], j['y'], 0.0))
				

		NewMesh = bpy.data.meshes.new("Point")
		NewMesh.from_pydata \
		(
			Vertices,
			[],
			[]
		)
		NewMesh.update()
		NewObj = bpy.data.objects.new("Path_NaviPoint", NewMesh)
		context.scene.objects.link(NewObj)
		
	def RenderPathNodes(self, context):
		Vertices = []
		for i in self.pathfiles:
			for j in i.Paths():
				Vertices.append((j['x'], j['y'], j['z']))
				

		NewMesh = bpy.data.meshes.new("Point")
		NewMesh.from_pydata \
		(
			Vertices,
			[],
			[]
		)
		NewMesh.update()
		NewObj = bpy.data.objects.new("Path_PathPoint", NewMesh)
		context.scene.objects.link(NewObj)
	
	def CleanScene(self):
		scene = bpy.context.scene
		
		for ob in scene.objects:
			if ob.type == 'MESH' and ob.name.startswith("Path"):
				ob.select = True
			else:
				ob.select = False

		
		bpy.ops.object.delete()
	
	def invoke(self, context, event):
		sce = bpy.context.scene
		obs = []

		
		for i in range(MAX_SEGMENT * MAX_SEGMENT):
			file = SAPath(r'F:\paths-visualizer\PathsVisualizer\Vanilla\BinaryPaths\SA' + '\\nodes' + str(i) + ".dat")
			self.pathfiles.append(file)
		
		self.CleanScene()
		self.RenderPathNodes(context)
#		self.RenderNaviNodes(context)
		#self.RenderNaviNodesBMesh(context)
		self.RenderNaviNodesLines(context)
		
		
		return {"FINISHED"}

bpy.utils.register_class(SAPathVisualizer)

class MakePoint(bpy.types.Operator) :
	bl_idname = "mesh.make_point"
	bl_label = "Add Point"

	def invoke(self, context, event) :
		Vertices = \
		[
			mathutils.Vector((0, -1 / math.sqrt(3),0)),
			mathutils.Vector((0.5, 1 / (2 * math.sqrt(3)), 0)),
			mathutils.Vector((-0.5, 1 / (2 * math.sqrt(3)), 0)),
			mathutils.Vector((0, 0, math.sqrt(2 / 3))),
		]
		NewMesh = bpy.data.meshes.new("Point")
		NewMesh.from_pydata \
		(
			Vertices,
			[],
			[]
		)
		NewMesh.update()
		NewObj = bpy.data.objects.new("Point", NewMesh)
		context.scene.objects.link(NewObj)
		return {"FINISHED"}
	#end invoke
#end MakeTetrahedron

class MakeTetrahedron(bpy.types.Operator) :
	bl_idname = "mesh.make_tetrahedron"
	bl_label = "Add Tetrahedron"

	def invoke(self, context, event) :
		Vertices = \
		[
			mathutils.Vector((0, -1 / math.sqrt(3),0)),
			mathutils.Vector((0.5, 1 / (2 * math.sqrt(3)), 0)),
			mathutils.Vector((-0.5, 1 / (2 * math.sqrt(3)), 0)),
			mathutils.Vector((0, 0, math.sqrt(2 / 3))),
		]
		NewMesh = bpy.data.meshes.new("Tetrahedron")
		NewMesh.from_pydata \
		(
			Vertices,
			[],
			[[0, 1, 2], [0, 1, 3], [1, 2, 3], [2, 0, 3]]
		)
		NewMesh.update()
		NewObj = bpy.data.objects.new("Tetrahedron", NewMesh)
		context.scene.objects.link(NewObj)
		return {"FINISHED"}
	#end invoke
#end MakeTetrahedron

bpy.utils.register_class(MakeTetrahedron)
bpy.utils.register_class(MakePoint)


