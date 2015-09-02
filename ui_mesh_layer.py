import bpy
import bmesh
from . import path_mesh_helper
from .ui_constants import *

def writeUpdateToVert(self, context):
    me = context.object.data
    bm = bmesh.from_edit_mesh(me)
    bmvert = bm.verts[self.index]
    
    #bmvert[bm.verts.layers.string[NODE_TYPE]]                = self.type
    #bmvert[bm.verts.layers.int[NODE_AREAID]]                 = self.area
    #bmvert[bm.verts.layers.int[NODE_ID]]                     = self.nodeid
    #bmvert[bm.verts.layers.int[NODE_FLOOD]]                  = self.flood
    
    bmvert[bm.verts.layers.float[NODE_WIDTH]]                = self.width
    bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]              = self.behaviour
    bmvert[bm.verts.layers.int[NODE_ISDEADEND]]              = self.isdeadEnd
    bmvert[bm.verts.layers.int[NODE_ISIGNORED]]              = self.isIgnoredNode
    bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]]            = self.isRoadBlock
    bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] = self.isEmergencyVehicleOnly
    bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]]     = self.isRestrictedAccess
    bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]]           = self.isDontWander
    bmvert[bm.verts.layers.int[NODE_SPEEDLIMIT]]             = self.speedlimit
    bmvert[bm.verts.layers.int[NODE_SPAWNPROBABILITY]]       = self.spawnProbability
    
    print("fuck")
    bmesh.update_edit_mesh(me, tessface=False, destructive=False)
    #bm.free()

def writeUpdateToEdge(self, context):
    me = context.object.data
    bm = bmesh.from_edit_mesh(me)
    bmedge = bm.edges[self.index]
    
    bmedge[bm.edges.layers.float[EDGE_WIDTH]]                = self.width
    bmedge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]           = self.LeftLanes
    bmedge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]          = self.RightLanes
    bmedge[bm.edges.layers.int[EDGE_ISTRAINCROSSING]]        = self.isTrainCrossing
    bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]]  = self.trafficLightDirection
    bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]]  = self.trafficLightBehaviour
    bmesh.update_edit_mesh(me, tessface=False, destructive=False)
    #bm.free()
    
class MeshVertLayer(bpy.types.PropertyGroup):
    index = bpy.props.IntProperty()

    width                            = bpy.props.FloatProperty(update=writeUpdateToVert)
    behaviour                        = bpy.props.IntProperty(update=writeUpdateToVert)
    isdeadEnd                        = bpy.props.BoolProperty(update=writeUpdateToVert)
    isIgnoredNode                    = bpy.props.BoolProperty(update=writeUpdateToVert)
    isRoadBlock                      = bpy.props.BoolProperty(update=writeUpdateToVert)
    isEmergencyVehicleOnly           = bpy.props.BoolProperty(update=writeUpdateToVert)
    isRestrictedAccess               = bpy.props.BoolProperty(update=writeUpdateToVert)
    isDontWander                     = bpy.props.BoolProperty(update=writeUpdateToVert)
    speedlimit                       = bpy.props.IntProperty(update=writeUpdateToVert)
    spawnProbability                 = bpy.props.IntProperty(update=writeUpdateToVert)
    type                             = bpy.props.StringProperty()
    area                             = bpy.props.IntProperty()
    nodeid                           = bpy.props.IntProperty()
    flood                            = bpy.props.IntProperty()
        
class MeshEdgeLayer(bpy.types.PropertyGroup):
    index = bpy.props.IntProperty()

    width                            = bpy.props.FloatProperty(update=writeUpdateToEdge)
    LeftLanes                        = bpy.props.IntProperty(update=writeUpdateToEdge)
    RightLanes                       = bpy.props.IntProperty(update=writeUpdateToEdge)
    isTrainCrossing                  = bpy.props.BoolProperty(update=writeUpdateToEdge)
    trafficLightDirection            = bpy.props.IntProperty(update=writeUpdateToEdge)
    trafficLightBehaviour            = bpy.props.IntProperty(update=writeUpdateToEdge)
    
class MeshLayer(bpy.types.PropertyGroup):
    index = bpy.props.IntProperty()
    
    isMyListOutdated = bpy.props.BoolProperty()
    vertList = bpy.props.CollectionProperty(type=MeshVertLayer)
    edgeList = bpy.props.CollectionProperty(type=MeshEdgeLayer)

# per vertex path node information viewer
class MESH_OT_layer_add(bpy.types.Operator):
    """Tooltip"""
    bl_label = "Add vert Layer"
    bl_idname = "mesh.layer_add"
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')

    def execute(self, context):
        bm = bmesh.from_edit_mesh(context.object.data)
        try:
            bm.verts.layers.float[NODE_WIDTH]
        except KeyError:
            path_mesh_helper.AddPathMeshLayers(bm)
        else:
            return {'CANCELLED'} 
        return {'FINISHED'}
    
class MeshVertLayerList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name)
            layout.label("area: " + str(item.area))
            layout.label("node: " +str(item.nodeid))
            layout.prop(item, "width", text="width", emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
            
class MeshEdgeLayerList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name)
            #layout.prop(item, "LeftLanes", text="LeftLanes", emboss=False)
            #layout.prop(item, "RightLanes", text="RightLanes", emboss=False)
            layout.label("LeftLanes: " + str(item.LeftLanes))
            layout.label("RightLanes: " +str(item.RightLanes))
            layout.prop(item, "width", text="width", emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
       
def UpdateCollectionOnReq(self, context):
    wm = context.window_manager
    wm.mesh_layer.vertList.clear()
    wm.mesh_layer.edgeList.clear()
    
    ob = context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    
    selectedVertices = [v.index for v in bm.verts if v.select]
    selectedEdges = [e.index for e in bm.edges if e.select]
    
    #if len(selectedVertices) > 20:
        #self.report({'ERROR'}, "fddf");
        #return
    
    wm.mesh_layer.isMyListOutdated = False
    
    for i in selectedVertices:
        item = wm.mesh_layer.vertList.add()
        item.name = "v #%i" %i
        item.index = i
        
        bmvert = bm.verts[i]
        item.width                    =    bmvert[bm.verts.layers.float[NODE_WIDTH]]               
        item.behaviour                =    bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]             
        item.isdeadEnd                =    bmvert[bm.verts.layers.int[NODE_ISDEADEND]]             
        item.isIgnoredNode            =    bmvert[bm.verts.layers.int[NODE_ISIGNORED]]             
        item.isRoadBlock              =    bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]]           
        item.isEmergencyVehicleOnly   =    bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]]
        item.isRestrictedAccess       =    bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]]    
        item.isDontWander             =    bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]]          
        item.speedlimit               =    bmvert[bm.verts.layers.int[NODE_SPEEDLIMIT]]            
        item.spawnProbability         =    bmvert[bm.verts.layers.int[NODE_SPAWNPROBABILITY]]      
        item.type                     =    bmvert[bm.verts.layers.string[NODE_TYPE]].decode()
        item.area                     =    bmvert[bm.verts.layers.int[NODE_AREAID]]                
        item.nodeid                   =    bmvert[bm.verts.layers.int[NODE_ID]]                    
        item.flood                    =    bmvert[bm.verts.layers.int[NODE_FLOOD]]   
    
    for i in selectedEdges:
        item = wm.mesh_layer.edgeList.add()
        item.name = "edge #%i" %i
        item.index = i
        
        bmedge = bm.edges[i]
        
        item.width                    =    bmedge[bm.edges.layers.float[EDGE_WIDTH]]   
        item.LeftLanes                =    bmedge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]          
        item.RightLanes               =    bmedge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]         
        item.isTrainCrossing          =    bmedge[bm.edges.layers.int[EDGE_ISTRAINCROSSING]]                     
        item.trafficLightDirection    =    bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]] 
        item.trafficLightBehaviour    =    bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]] 
    
def CheckIfListOutdated(context):
    wm = context.window_manager
    
    if wm.mesh_layer.isMyListOutdated:
        return True
        
    ob = context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    
    selectedVertices = [v.index for v in bm.verts if v.select]
    selectedEdges = [e.index for e in bm.edges if e.select] 
    
    myVertList = [x.index for x in wm.mesh_layer.vertList] 
    myEdgeList = [x.index for x in wm.mesh_layer.edgeList]
    
    if set(selectedVertices) == set(myVertList) and set(selectedEdges) == set(myEdgeList):
        wm.mesh_layer.isMyListOutdated = False
        return False
    else:
        wm.mesh_layer.isMyListOutdated = True
        return True
    
class display_editable_list_operator(bpy.types.Operator):
    """Test exporter which just writes hello world"""
    bl_idname = "paths.display_selected_for_edit"
    bl_label = "Display Selected"

    def execute(self, context):
        UpdateCollectionOnReq(self, context)
        return {'FINISHED'}
        
# TODO: Find a way to update list per selection change event not every draw event
class PathNodePropertiesPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Path Ultimatum: PathNode"
    bl_idname = "OBJECT_PT_pathnode"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        try:
            bm.verts.layers.float[NODE_WIDTH]
        except KeyError:
            layout.label("This is not a path mesh.")
            layout.operator("mesh.layer_add")
            return
        
        if bm.select_mode != {'VERT'}:
            layout.label("Vertex select only", icon = 'INFO')
            return
        
        row = layout.row(align=True)
        props = row.operator("paths.display_selected_for_edit")
        
        #if CheckIfListOutdated(context):
            #return
           
        layout.label(text="Node Attributes")
        layout.template_list("MeshVertLayerList", "", wm.mesh_layer, "vertList", wm.mesh_layer, "index")
        
        layout.label(text="Edge Attributes")
        layout.template_list("MeshEdgeLayerList", "", wm.mesh_layer, "edgeList", wm.mesh_layer, "index")


def setupProps():
    bpy.types.WindowManager.mesh_layer = bpy.props.PointerProperty(type=MeshLayer)
    
def removeProps():
    del bpy.types.WindowManager.mesh_layer

def register():
    bpy.utils.register_module(__name__)
    setupProps()

def unregister():
    bpy.utils.unregister_module(__name__)
    removeProps()

if __name__ == "__main__":
    register()