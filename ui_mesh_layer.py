import bpy
import bmesh
from . import path_mesh_helper
from .ui_constants import *
    
class MeshVertLayer(bpy.types.PropertyGroup):
    def writeVertexWidth(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.float[NODE_WIDTH]] = self.width
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
    
    def writeVertexBehaviour(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_BAHAVIOUR]] = self.behaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexIsdeadEnd(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISDEADEND]] = self.behaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexIsIgnoredNode(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISIGNORED]] = self.isIgnoredNode
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexIsRoadBlock(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISROADBLOCK]] = self.isRoadBlock
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexIsEmergencyVehicleOnly(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] = self.isEmergencyVehicleOnly
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexIsRestrictedAccess(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]] = self.isRestrictedAccess
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexIsDontWander(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISDONTWANDER]] = self.isDontWander
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexSpeedlimit(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_SPEEDLIMIT]] = self.speedlimit
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeVertexSpawnProbability(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_SPAWNPROBABILITY]] = self.spawnProbability
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    index = bpy.props.IntProperty()

    width                            = bpy.props.FloatProperty(update=writeVertexWidth)
    behaviour                        = bpy.props.IntProperty(update=writeVertexBehaviour)
    isdeadEnd                        = bpy.props.BoolProperty(update=writeVertexIsdeadEnd)
    isIgnoredNode                    = bpy.props.BoolProperty(update=writeVertexIsIgnoredNode)
    isRoadBlock                      = bpy.props.BoolProperty(update=writeVertexIsRoadBlock)
    isEmergencyVehicleOnly           = bpy.props.BoolProperty(update=writeVertexIsEmergencyVehicleOnly)
    isRestrictedAccess               = bpy.props.BoolProperty(update=writeVertexIsRestrictedAccess)
    isDontWander                     = bpy.props.BoolProperty(update=writeVertexIsDontWander)
    speedlimit                       = bpy.props.IntProperty(update=writeVertexSpeedlimit)
    spawnProbability                 = bpy.props.IntProperty(update=writeVertexSpawnProbability)
    
    type                             = bpy.props.StringProperty()
    area                             = bpy.props.IntProperty()
    nodeid                           = bpy.props.IntProperty()
    flood                            = bpy.props.IntProperty()
        
class MeshEdgeLayer(bpy.types.PropertyGroup):
    def writeEdgeWidth(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.float[EDGE_WIDTH]] = self.width
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeEdgeLeftLanes(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_NUMLEFTLANES]] = self.LeftLanes
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeEdgeRightLanes(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_NUMRIGHTLANES]] = self.RightLanes
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeEdgeTrainCross(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_ISTRAINCROSSING]] = self.isTrainCrossing
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeEdgeTRL_DIR(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]] = self.trafficLightDirection
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def writeEdgeTRL_BEH(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]] = self.trafficLightBehaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    index = bpy.props.IntProperty()

    width                            = bpy.props.FloatProperty(update=writeEdgeWidth)
    LeftLanes                        = bpy.props.IntProperty(update=writeEdgeLeftLanes)
    RightLanes                       = bpy.props.IntProperty(update=writeEdgeRightLanes)
    isTrainCrossing                  = bpy.props.BoolProperty(update=writeEdgeTrainCross)
    trafficLightDirection            = bpy.props.IntProperty(update=writeEdgeTRL_DIR)
    trafficLightBehaviour            = bpy.props.IntProperty(update=writeEdgeTRL_BEH)
    
class MeshLayer(bpy.types.PropertyGroup):
    vIndex = bpy.props.IntProperty()
    eIndex = bpy.props.IntProperty()
    
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
            layout.prop(item, "behaviour", text="behaviour", emboss=False)
            layout.prop(item, "isdeadEnd", text="isdeadEnd", emboss=False)
            layout.prop(item, "isIgnoredNode", text="isIgnoredNode", emboss=False)
            layout.prop(item, "isRoadBlock", text="isRoadBlock", emboss=False)
            layout.prop(item, "isEmergencyVehicleOnly", text="isEmergencyVehicleOnly", emboss=False)
            layout.prop(item, "isRestrictedAccess", text="isRestrictedAccess", emboss=False)
            layout.prop(item, "isDontWander", text="isDontWander", emboss=False)
            layout.prop(item, "speedlimit", text="speedlimit", emboss=False)
            layout.prop(item, "spawnProbability", text="spawnProbability", emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
            
class MeshEdgeLayerList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name)
            layout.prop(item, "LeftLanes", text="LeftLanes", emboss=False)
            layout.prop(item, "RightLanes", text="RightLanes", emboss=False)
            #layout.label("LeftLanes: " + str(item.LeftLanes))
            #layout.label("RightLanes: " +str(item.RightLanes))
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
   
    for i in selectedVertices:
        item = wm.mesh_layer.vertList.add()
        item.name = "v #%i" %i
        item.index = i
        
        bmvert = bm.verts[i]
        item.width                    =    bmvert[bm.verts.layers.float[NODE_WIDTH]]               
        item.behaviour                =    bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]             
        item.isdeadEnd                =    bmvert[bm.verts.layers.int[NODE_ISDEADEND]] == 1
        item.isIgnoredNode            =    bmvert[bm.verts.layers.int[NODE_ISIGNORED]] == 1
        item.isRoadBlock              =    bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]] == 1
        item.isEmergencyVehicleOnly   =    bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] == 1
        item.isRestrictedAccess       =    bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]] == 1
        item.isDontWander             =    bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]] == 1
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
           
        layout.label(text="Node Attributes")
        layout.template_list("MeshVertLayerList", "", wm.mesh_layer, "vertList", wm.mesh_layer, "vIndex")
        
        layout.label(text="Edge Attributes")
        layout.template_list("MeshEdgeLayerList", "", wm.mesh_layer, "edgeList", wm.mesh_layer, "eIndex")


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