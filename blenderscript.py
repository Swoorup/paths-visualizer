import math 
import bpy
import bmesh
import itertools
import mathutils
from sapaths import SAPaths

MAX_SEGMENT = 8
BLOCK_SIZE = 750.0

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
    
def BmeshPlane():
    me = bpy.data.meshes.new('BmeshPlane') 
    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh
                
    # Hot to create vertices
    #vertex1 = bm.verts.new( (-0.5, -0.5, 0.0) )
    #vertex2 = bm.verts.new( (0.5, -0.5, 0.0) )
    #vertex3 = bm.verts.new( (0.5, 0.5, 0.0) )
    #vertex4 = bm.verts.new( (-0.5, 0.5, 0.0) )
            
    vertex = bm.verts.new( (0.0, 0.0, 0.0) )
    # Initialize the index values of this sequence.
    bm.verts.index_update()
    
    # How to create edges    
    #bm.edges.new( (vertex1, vertex2) )
    #bm.edges.new( (vertex2, vertex3) )
    #bm.edges.new( (vertex3, vertex4) )
    #bm.edges.new( (vertex4, vertex1) )
        
    # How to create a face
    # it's not necessary to create the edges before, I made it only to show how create 
    # edges too
    #bm.faces.new( (vertex1, vertex2, vertex3, vertex4))
        
    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    return me

def BmeshTriangle():
    me = bpy.data.meshes.new('BmeshTriangle') 
    # Get a BMesh representation
    bm = bmesh.new()   # create an empty BMesh
    bm.from_mesh(me)   # fill it in from a Mesh
                
    # Hot to create vertices
    #vertex1 = bm.verts.new( (-0.5, -0.5, 0.0) )
    #vertex2 = bm.verts.new( (0.5, -0.5, 0.0) )
    #vertex3 = bm.verts.new( (0.0, 0.5, 0.0) )
    
    vertex = bm.verts.new( (0.0, 0.0, 0.0) )
            
    # Initialize the index values of this sequence.
    bm.verts.index_update()
    
    # How to create edges    
    #bm.edges.new( (vertex1, vertex2) )
    #bm.edges.new( (vertex2, vertex3) )
    #bm.edges.new( (vertex3, vertex1) )
        
    # How to create a face
    # it's not necessary to create the edges before, I made it only to show how create 
    # edges too
    #bm.faces.new( (vertex1, vertex2, vertex3))
        
    # Finish up, write the bmesh back to the mesh
    bm.to_mesh(me)
    return me

def PointCloud(Vertices, name, context):
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

class SAPathVisualizer(bpy.types.Operator) :
    bl_idname = "mesh.makepaths"
    bl_label = "Make paths"
    
    binaryNodesDir = ""
    
    def __init__(self):
        self.path = SAPaths()
    
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
        for i in self.path.vehiclePathNodes:
            Vertices.append((i.x, i.y, i.z))
                
        PointCloud(Vertices, "vehicleNodes", context)
    
    def CleanScene(self):
        scene = bpy.context.scene
        
        for ob in scene.objects:
            if ob.type == 'MESH' and ob.name.startswith("Path"):
                ob.select = True
            else:
                ob.select = False
        
        bpy.ops.object.delete()
    
    def invoke(self, context, event):
        self.path = SAPaths()
        self.path.LoadFromDirectory(r'E:\Output')
        
        self.CleanScene()
        self.RenderPathNodes(context)
        #self.RenderNaviNodesBMesh(context)
        
        return {"FINISHED"}

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
        

class SAPathViewerPanel(bpy.types.Panel):
    """Creates a Panel in the World properties window"""
    bl_label = "GTA SA Paths Viewer Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"

    def draw(self, context):
        layout = self.layout
        
        obj = context.object
        
        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')
        
        #row = layout.row()
        #row.label(text="Active object is: " + obj.name)
        #row = layout.row()
        #row.prop(obj, "name")
        
        row = layout.row()
        row.operator("mesh.primitive_cube_add")
        
        row = layout.row()
        row.operator("mesh.make_tetrahedron")
        
        row = layout.row()
        row.prop(context.scene, 'conf_path')
        
def register():
    bpy.utils.register_class(MakeTetrahedron)
    bpy.utils.register_class(MakePoint)
    bpy.utils.register_class(SAPathVisualizer)
    
    bpy.utils.register_class(SAPathViewerPanel)
    bpy.types.Scene.conf_path = bpy.props.StringProperty \
    (
    name = "Root Path",
    default = r'F:\paths-visualizer\PathsVisualizer\Vanilla\BinaryPaths\SA',
    description = "Define the root path of the project",
    subtype = 'DIR_PATH'
    )

def unregister():
    bpy.utils.unregister_class(MakeTetrahedron)
    bpy.utils.unregister_class(MakePoint)
    bpy.utils.unregister_class(SAPathVisualizer)
    bpy.utils.unregister_class(SAPathViewerPanel)

if __name__ == "__main__":
    register()