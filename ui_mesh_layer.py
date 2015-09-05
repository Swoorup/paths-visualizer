import bpy
import bmesh
from . import path_mesh_helper
from .ui_constants import *
from bpy.props import StringProperty, BoolProperty, IntProperty, CollectionProperty, FloatProperty, PointerProperty
    
class MeshVertLayer(bpy.types.PropertyGroup):
    def updateVertWidth(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.float[NODE_WIDTH]] = self.width
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
    
    def updateVertBehaviour(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_BAHAVIOUR]] = self.behaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsdeadEnd(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISDEADEND]] = self.behaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsIgnoredNode(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISIGNORED]] = self.isIgnoredNode
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsRoadBlock(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISROADBLOCK]] = self.isRoadBlock
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsEmergencyVehicleOnly(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] = self.isEmergencyVehicleOnly
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsRestrictedAccess(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]] = self.isRestrictedAccess
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertIsDontWander(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_ISDONTWANDER]] = self.isDontWander
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertSpeedlimit(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_SPEEDLIMIT]] = self.speedlimit
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateVertSpawnProbability(self, context):
        me = context.object.data
        bm=bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.int[NODE_SPAWNPROBABILITY]] = self.spawnProbability
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    index = IntProperty()

    width                            = FloatProperty(soft_min=0.0, soft_max=31, update=updateVertWidth)
    behaviour                        = IntProperty(update=updateVertBehaviour)
    isdeadEnd                        = BoolProperty(update=updateVertIsdeadEnd)
    isIgnoredNode                    = BoolProperty(update=updateVertIsIgnoredNode)
    isRoadBlock                      = BoolProperty(update=updateVertIsRoadBlock)
    isEmergencyVehicleOnly           = BoolProperty(update=updateVertIsEmergencyVehicleOnly)
    isRestrictedAccess               = BoolProperty(update=updateVertIsRestrictedAccess)
    isDontWander                     = BoolProperty(update=updateVertIsDontWander)
    speedlimit                       = IntProperty(soft_min=0, soft_max=3, update=updateVertSpeedlimit)
    spawnProbability                 = IntProperty(soft_min=0, soft_max=15, update=updateVertSpawnProbability)
    
    type                             = StringProperty()
    area                             = IntProperty()
    nodeid                           = IntProperty()
    flood                            = IntProperty()
        
class MeshEdgeLayer(bpy.types.PropertyGroup):
    def updateEdgeWidth(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.float[EDGE_WIDTH]] = self.width
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeLeftLanes(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_NUMLEFTLANES]] = self.LeftLanes
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeRightLanes(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_NUMRIGHTLANES]] = self.RightLanes
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeTrainCross(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_ISTRAINCROSSING]] = self.isTrainCrossing
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeTRL_DIR(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]] = self.trafficLightDirection
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    def updateEdgeTRL_BEH(self, context):
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.edges[self.index][bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]] = self.trafficLightBehaviour
        bmesh.update_edit_mesh(me, tessface=False, destructive=False)
        
    index = IntProperty()

    width                            = FloatProperty(soft_min=0.0, soft_max=31, update=updateEdgeWidth)
    LeftLanes                        = IntProperty(soft_min=0, soft_max=7, update=updateEdgeLeftLanes)
    RightLanes                       = IntProperty(soft_min=0, soft_max=7, update=updateEdgeRightLanes)
    isTrainCrossing                  = BoolProperty(update=updateEdgeTrainCross)
    trafficLightDirection            = IntProperty(update=updateEdgeTRL_DIR)
    trafficLightBehaviour            = IntProperty(update=updateEdgeTRL_BEH)
    
class MeshLayer(bpy.types.PropertyGroup):
    currentObj = StringProperty()
    
    bSelectOnListClick = BoolProperty(default=False)

    vIndex = IntProperty()
    eIndex = IntProperty()
    
    vertList = CollectionProperty(type=MeshVertLayer)
    edgeList = CollectionProperty(type=MeshEdgeLayer)

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
    
prevVertSelection = -1
class MeshVertLayerList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.scale_x = 0.5
            row.scale_y = 1
            row.label(item.name)
            row.label("A:" + str(item.area) + " N: " + str(item.nodeid))
            row.label("F:" + str(item.flood) + " T: " + str(item.type))
            row.prop(item, "width", text="width", emboss=False)
            row.prop(item, "behaviour", text="behaviour", emboss=False)
            row.prop(item, "isdeadEnd", text="DeadEnd", emboss=False)
            row.prop(item, "isIgnoredNode", text="Ignore", emboss=False)
            row.prop(item, "isRoadBlock", text="RoadBlock", emboss=False)
            row.prop(item, "isEmergencyVehicleOnly", text="EmergencyVehicle", emboss=False)
            row.prop(item, "isRestrictedAccess", text="Restricted", emboss=False)
            row.prop(item, "isDontWander", text="DontWander", emboss=False)
            row.prop(item, "speedlimit", text="speed", emboss=False)
            row.prop(item, "spawnProbability", text="spawn", emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
        
        wm = context.window_manager
        vertList = wm.mesh_layer.vertList
        vIndex = wm.mesh_layer.vIndex
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        global prevVertSelection
        if prevVertSelection == vIndex or wm.mesh_layer.bSelectOnListClick == False:
            return
        
        print("Changing vert for " + ob.name + "from: " + str(prevVertSelection) + " to: " + str(vIndex))
        if item.index != -1 and len(vertList) > 0:
            for i in range(len(vertList)):
                if i != vIndex:
                    bm.verts[vertList[i].index].select = False
        
            bm.verts[vertList[vIndex].index].select = True
        prevVertSelection = vIndex

prevEdgeSelection = -1        
class MeshEdgeLayerList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.scale_x = 0.5
            row.scale_y = 1
            row.label(item.name)
            row.prop(item, "LeftLanes", text="LeftLanes", emboss=False)
            row.prop(item, "RightLanes", text="RightLanes", emboss=False)
            row.prop(item, "width", text="width", emboss=False)
            
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
        
        wm = context.window_manager
        edgeList = wm.mesh_layer.edgeList
        eIndex = wm.mesh_layer.eIndex
        ob = context.object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        
        global prevEdgeSelection
        if prevEdgeSelection == eIndex or wm.mesh_layer.bSelectOnListClick == False:
            return
        
        print("Changing edge for " + ob.name + "from: " + str(prevEdgeSelection) + " to: " + str(eIndex))
        if item.index != -1 and len(edgeList) > 0:
            for i in range(len(edgeList)):
                if i != eIndex:
                    bm.edges[edgeList[i].index].select = False
        
            bm.edges[edgeList[eIndex].index].select = True
        prevEdgeSelection = eIndex
        
def ClearCollection(context):
    wm = context.window_manager
    
    wm.mesh_layer.vertList.clear()
    wm.mesh_layer.edgeList.clear()

    wm.mesh_layer.vIndex = -1
    wm.mesh_layer.eIndex = -1
    
    global prevEdgeSelection, prevVertSelection
    prevVertSelection = -1
    prevEdgeSelection = -1
    
def ClearCollectionIfNecessary(context):
    objname = bpy.context.object.name
    wm = context.window_manager

    if context.object is None:
        ClearCollection(context)
        return

    if context.object.type != 'MESH' or context.object.mode != 'EDIT':
        ClearCollection(context)
        return
    
    if (wm.mesh_layer.currentObj != objname): 
        ClearCollection(context)
        return

def UpdateCollectionOnReq(self, context):
    wm = context.window_manager
    ClearCollection(context)
    
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
        item.width                    = bmvert[bm.verts.layers.float[NODE_WIDTH]]               
        item.behaviour                = bmvert[bm.verts.layers.int[NODE_BAHAVIOUR]]             
        item.isdeadEnd                = bmvert[bm.verts.layers.int[NODE_ISDEADEND]] == 1
        item.isIgnoredNode            = bmvert[bm.verts.layers.int[NODE_ISIGNORED]] == 1
        item.isRoadBlock              = bmvert[bm.verts.layers.int[NODE_ISROADBLOCK]] == 1
        item.isEmergencyVehicleOnly   = bmvert[bm.verts.layers.int[NODE_ISEMERGENCYVEHICLEONLY]] == 1
        item.isRestrictedAccess       = bmvert[bm.verts.layers.int[NODE_ISRESTRICTEDACCESS]] == 1
        item.isDontWander             = bmvert[bm.verts.layers.int[NODE_ISDONTWANDER]] == 1
        item.speedlimit               = bmvert[bm.verts.layers.int[NODE_SPEEDLIMIT]]            
        item.spawnProbability         = bmvert[bm.verts.layers.int[NODE_SPAWNPROBABILITY]]      
        item.type                     = bmvert[bm.verts.layers.string[NODE_TYPE]].decode()
        item.area                     = bmvert[bm.verts.layers.int[NODE_AREAID]]                
        item.nodeid                   = bmvert[bm.verts.layers.int[NODE_ID]]                    
        item.flood                    = bmvert[bm.verts.layers.int[NODE_FLOOD]]   
    
    for i in selectedEdges:
        item = wm.mesh_layer.edgeList.add()
        item.name = "e #%i" %i
        item.index = i
        
        bmedge = bm.edges[i]
        
        item.width                    = bmedge[bm.edges.layers.float[EDGE_WIDTH]]   
        item.LeftLanes                = bmedge[bm.edges.layers.int[EDGE_NUMLEFTLANES]]          
        item.RightLanes               = bmedge[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]         
        item.isTrainCrossing          = bmedge[bm.edges.layers.int[EDGE_ISTRAINCROSSING]]                     
        item.trafficLightDirection    = bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTDIRECTION]] 
        item.trafficLightBehaviour    = bmedge[bm.edges.layers.int[EDGE_TRAFFICLIGHTBEHAVIOUR]] 
    
    objname = bpy.context.object.name
    wm.mesh_layer.currentObj = objname
    
class display_editable_list_operator(bpy.types.Operator):
    bl_idname = "paths.display_selected"
    bl_label = "List/Refresh Properties"

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')
        
    def execute(self, context):
        print("Displaying node/edge attributes")
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
        return True

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        ClearCollectionIfNecessary(context)
        ob = context.object

        if (context.object is None or
                context.object.type != 'MESH' or
                context.object.mode != 'EDIT'):
            return

        me = ob.data
        bm = bmesh.from_edit_mesh(me)
        try:
            bm.verts.layers.float[NODE_WIDTH]
        except KeyError:
            layout.label("This is not a path mesh.")
            layout.operator("mesh.layer_add")
            return

        selectedMode = 'Vertex'

        if bm.select_mode == {'EDGE'}:
            selectedMode = 'Edge'
        
        if bm.select_mode != {'VERT'} and bm.select_mode != {'EDGE'}:
            layout.label("Vertex or Edge select only", icon = 'INFO')
            return
        
        layout.label(text="Selected " + selectedMode+"(s)")
        row = layout.row(align=True)
        row.scale_y = 1.5
        props = row.operator(display_editable_list_operator.bl_idname)
        row.prop(wm.mesh_layer, "bSelectOnListClick", text="Select " + selectedMode+"(s)" + " on Highlight")
        
        if bm.select_mode == {'VERT'}:
            layout.label(text="Node Attributes")
            layout.template_list("MeshVertLayerList", "", wm.mesh_layer, "vertList", wm.mesh_layer, "vIndex")
        
        layout.label(text="Edge Attributes")
        layout.template_list("MeshEdgeLayerList", "", wm.mesh_layer, "edgeList", wm.mesh_layer, "eIndex")


addon_keymaps = []
def setupProps():
    bpy.types.WindowManager.mesh_layer = PointerProperty(type=MeshLayer)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi = km.keymap_items.new(display_editable_list_operator.bl_idname, 'Q', 'PRESS', alt=True)
    addon_keymaps.append(km)
    
def removeProps():
    del bpy.types.WindowManager.mesh_layer
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()

def register():
    bpy.utils.register_module(__name__)
    setupProps()
    
def unregister():
    bpy.utils.unregister_module(__name__)
    removeProps()

if __name__ == "__main__":
    register()