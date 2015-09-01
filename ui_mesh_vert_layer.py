import bpy
import bmesh
from . import path_mesh_helper
from .ui_constants import *

def writeUpdateToVert(self, context):
    try:
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bmvert = bm.verts[self.index]
        
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
        bmvert[bm.verts.layers.int[NODE_NUMLEFTLANES]]           = self.LeftLanes
        bmvert[bm.verts.layers.int[NODE_NUMRIGHTLANES]]          = self.RightLanes
        bmvert[bm.verts.layers.int[NODE_ISTRAINCROSSING]]        = self.isTrainCrossing
        #bmvert[bm.verts.layers.string[NODE_TYPE]]                = self.type
        #bmvert[bm.verts.layers.int[NODE_AREAID]]                 = self.area
        #bmvert[bm.verts.layers.int[NODE_ID]]                     = self.nodeid
        #bmvert[bm.verts.layers.int[NODE_FLOOD]]                  = self.flood
        bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTDIRECTION]]  = self.trafficLightDirection
        bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTBEHAVIOUR]]  = self.trafficLightBehaviour
        
        bmesh.update_edit_mesh(me, tessvert=False, destructive=False)
    except:
        pass


class MeshVertLayervert(bpy.types.PropertyGroup):
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
    LeftLanes                        = bpy.props.IntProperty(update=writeUpdateToVert)
    RightLanes                       = bpy.props.IntProperty(update=writeUpdateToVert)
    isTrainCrossing                  = bpy.props.BoolProperty(update=writeUpdateToVert)
    type                             = bpy.props.StringProperty()
    area                             = bpy.props.IntProperty()
    nodeid                           = bpy.props.IntProperty()
    flood                            = bpy.props.IntProperty()
    trafficLightDirection            = bpy.props.IntProperty(update=writeUpdateToVert)
    trafficLightBehaviour            = bpy.props.IntProperty(update=writeUpdateToVert)
    
    
class MeshVertLayer(bpy.types.PropertyGroup):
    index = bpy.props.IntProperty()
    vertList = bpy.props.CollectionProperty(type=MeshVertLayervert)

# per vertex path node information viewer
class MESH_OT_vert_layer_add(bpy.types.Operator):
    """Tooltip"""
    bl_label = "Add vert Layer"
    bl_idname = "mesh.vert_layer_add"
    
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
            path_mesh_helper.AddPathMeshVertLayers(bm)
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
    
def UpdateCollectionIfNecessary(selected, vertCollection, bm):
    vertlist = [x.index for x in vertCollection]
    
    if set(vertlist) != set(selected):
    
        # these make blender crawl
        bm.verts.ensure_lookup_table()
        vertCollection.clear()
        for i in selected:
            item = vertCollection.add()
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
            item.LeftLanes                =    bmvert[bm.verts.layers.int[NODE_NUMLEFTLANES]]          
            item.RightLanes               =    bmvert[bm.verts.layers.int[NODE_NUMRIGHTLANES]]         
            item.isTrainCrossing          =    bmvert[bm.verts.layers.int[NODE_ISTRAINCROSSING]]       
            item.type                     =    bmvert[bm.verts.layers.string[NODE_TYPE]].decode()
            item.area                     =    bmvert[bm.verts.layers.int[NODE_AREAID]]                
            item.nodeid                   =    bmvert[bm.verts.layers.int[NODE_ID]]                    
            item.flood                    =    bmvert[bm.verts.layers.int[NODE_FLOOD]]                 
            item.trafficLightDirection    =    bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTDIRECTION]] 
            item.trafficLightBehaviour    =    bmvert[bm.verts.layers.int[NODE_TRAFFICLIGHTBEHAVIOUR]] 
                
        
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
            layout.label("No custom data layer 'test'.")
            layout.operator("mesh.vert_layer_add")
            return
        
        if bm.select_mode != {'VERT'}:
            layout.label("Vertex select only", icon = 'INFO')
            return
        
        # use kd trees here or maybe a simple grid and then raycast??
        selected = []
        for vert in bm.verts:
            if vert.select:
                selected.append(vert.index)
                # restricted because of performance issues
                if len(selected) > 10:
                    layout.label("To display properties please select less than 10 vertices", icon = 'INFO')
                    return
        
        
        if not selected:
            layout.label("Nothing selected", icon = 'INFO')
            return
        
        UpdateCollectionIfNecessary(selected, wm.mesh_vert_layer.vertList, bm)
                
        layout.template_list("MeshVertLayerList", "", wm.mesh_vert_layer, "vertList", wm.mesh_vert_layer, "index")


def setupProps():
    bpy.types.WindowManager.mesh_vert_layer = bpy.props.PointerProperty(type=MeshVertLayer)
    
def removeProps():
    del bpy.types.WindowManager.mesh_vert_layer

def register():
    bpy.utils.register_module(__name__)
    setupProps()

def unregister():
    bpy.utils.unregister_module(__name__)
    removeProps()

if __name__ == "__main__":
    register()