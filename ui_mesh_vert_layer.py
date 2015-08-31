import bpy
import bmesh

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
            bm.verts.layers.float['test']
            node_width_key = bm.verts.layers.float['node_width']
            node_area_id = bm.verts.layers.int['node_areaid']
            node_node_id = bm.verts.layers.int['node_id']
            node_behaviour = bm.verts.layers.int['node_behaviour']
        except KeyError:
            bm.verts.layers.float.new('test')
        else:
            return {'CANCELLED'}
            
        return {'FINISHED'}
    

class MeshVertLayerList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(item.name)
            layout.label(item.fuck)
            layout.prop(item, "value", text="", emboss=False)

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="")
    
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
            l = bm.verts.layers.float['test']
        except KeyError:
            layout.label("No custom data layer 'test'.")
            layout.operator("mesh.vert_layer_add")
            return
        
        if bm.select_mode != {'VERT'}:
            layout.label("Vertex select only", icon = 'INFO')
            return
        
        selected = [vert.index for vert in bm.verts if vert.select]
        if not selected:
            layout.label("Nothing selected", icon = 'INFO')
            return
        
        # restricted because of performance issues
        if len(selected) > 20:
            layout.label("To display properties please select less than 20 vertices", icon = 'INFO')
            return
        
        vertlist = [x.index for x in wm.mesh_vert_layer.verts]

        if set(vertlist) != selected:
            wm.mesh_vert_layer.verts.clear()
            for v in selected:
                item = wm.mesh_vert_layer.verts.add()
                item.name = "vert #%i" %v.index
                item.index = v.index
                item.value = v[l]
                item.fuck = "dss"
                
        layout.template_list("MeshVertLayerList", "", wm.mesh_vert_layer, "verts", wm.mesh_vert_layer, "index")


def upd(self, context):
    try:
        me = context.object.data
        bm = bmesh.from_edit_mesh(me)
        bm.verts[self.index][bm.verts.layers.float['test']] = self.value
        bmesh.update_edit_mesh(me, tessvert=False, destructive=False)
    except:
        pass

class MeshVertLayervert(bpy.types.PropertyGroup):
    value = bpy.props.FloatProperty(update=upd)
    index = bpy.props.IntProperty()
    fuck = bpy.props.StringProperty()

    
class MeshVertLayer(bpy.types.PropertyGroup):
    index = bpy.props.IntProperty()
    verts = bpy.props.CollectionProperty(type=MeshVertLayervert)

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