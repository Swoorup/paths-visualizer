import bpy
import blenderscript
import bmesh

from bpy.props import IntProperty, CollectionProperty
from bpy.types import Panel, UIList

import imp
imp.reload(blenderscript)

"""

GTA SA: sa_nodes_loader_operator
GTA VC: ipl_paths_loader_operator
GTA IV: iv_nodes_loader_operator
 
"""
# nodes mesh information apply
class ApplyVertCol(bpy.types.Operator):
    bl_idname = "vertex_col.apply"
    bl_label = "Assign"
    bl_description = "Assign color to selected vertices for selected vertex color layer"

    def execute(self, context):
        me = context.active_object.data
        bm = bmesh.from_edit_mesh(me)
        selected = [vert.index for vert in bm.verts if vert.select]
        bpy.ops.object.mode_set(mode='EDIT', toggle=True)
        for face in me.polygons:
            for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
                if vert_idx in selected:
                    me.vertex_colors[me.vertex_colors.active_index].data[loop_idx].color = context.scene.color_picker
        bpy.ops.object.mode_set(mode='EDIT', toggle=True)
        return{'FINISHED'}

# nodes mesh information viewer
class path_mesh_viewer_panel(bpy.types.Panel):
    #bl_space_type = 'VIEW_3D'
    #bl_region_type = 'UI'
    #bl_label = "3D Cursor"
    bl_label = "Path Node"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context):
        return (context.active_object is not None and 
                context.mode=="EDIT_MESH")

    def draw(self, context):
        layout = self.layout
        
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].clip_end = 100000
                area.spaces[0].grid_lines = 8
                area.spaces[0].grid_scale = 750
                area.spaces[0].grid_subdivisions = 1
                
                view = area.spaces[0]
                layout.column().prop(view, "cursor_location", text="Location")

        ob = bpy.context.active_object
        me = ob.data
        bm = bmesh.from_edit_mesh(me)

        node_width_key = bm.verts.layers.float['node_width']
        node_area_id = bm.verts.layers.int['node_areaid']
        node_node_id = bm.verts.layers.int['node_id']
        node_behaviour = bm.verts.layers.int['node_behaviour']

        # Set/retrieve the values at a particular vert/edge/face/loop
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()

        if bm.select_mode != {'VERT'}:
            layout.label("Vertex select only", icon = 'INFO')
            return

        selected = [vert.index for vert in bm.verts if vert.select]
        if not selected:
            layout.label("Nothing selected", icon = 'INFO')
        else:
            row = layout.row(align=True)
            for i in selected:
                print(bm.verts[i][node_area_id], 
                      bm.verts[i][node_node_id],
                      bm.verts[i][node_width_key],
                      bm.verts[i][node_behaviour]
                      )
            #row.prop(context.scene, 'color_picker', text="")
            #row.operator("vertex_col.apply")
            
            #for i in selected:
                #layout.column().prop(bm.verts[i][key1], "", text = 'INFO')

       # bmesh.update_edit_mesh(me, True)
        #bm.free()

class Zone(bpy.types.PropertyGroup):
    # name = StringProperty()
    id = IntProperty()

#set up blender grid to match path grid
class setup_scene_for_paths_op(bpy.types.Operator):
    bl_idname = "setup.setup_scene_for_paths_op"
    bl_label = "Setup grid to match path nodes"

    def execute(self, context):
        for area in bpy.context.screen.areas:
            print(area.type)
            if area.type == 'VIEW_3D':
                area.spaces[0].clip_end = 100000
                area.spaces[0].grid_lines = 8
                area.spaces[0].grid_scale = 750
                area.spaces[0].grid_subdivisions = 1
        return {'FINISHED'}


class sa_nodes_loader_operator(bpy.types.Operator):
    bl_idname = "loader.sa_nodes_loader_operator"
    bl_label = "Load GTA SA Nodes file format"

    path = bpy.props.StringProperty(name="sa_nodes_path")

    #@classmethod
    #def poll(cls, context):
        #return context.active_object is not None

    def execute(self, context):
        blenderscript.loadSAPathsAsMesh(self.path)
        return {'FINISHED'}

class ipl_paths_loader_operator(bpy.types.Operator):
    """Test exporter which just writes hello world"""
    bl_idname = "loader.ipl_paths_loader_operator"
    bl_label = "Export Some Data"

    filepath = bpy.props.StringProperty(subtype="DIR_PATH")

    #@classmethod
    #def poll(cls, context):
        #return context.object is not None

    def execute(self, context):
        #file = open(self.filepath, 'w')
        #file.write("Hello World " + context.object.name)
        self.report({'ERROR'}, "fddf");
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PathsUltimatumPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "GTA Path Ultimatum"
    bl_idname = "OBJECT_PT_PathsUltimatum"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        # Create a simple row.
        layout.label(text=" Simple Row:")

        row = layout.row()
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create an row where the buttons are aligned to each other.
        layout.label(text=" Aligned Row:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")

        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column()
        col.label(text="Column One:")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_start")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Column Two:")
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")

        # Big render button
        layout.label(text="Big Button:")
        row = layout.row()
        row.scale_y = 3.0
        row.operator("setup.setup_scene_for_paths_op")


        # Different sizes in a row
        layout.label(text="Load SA Nodes:")
        row = layout.row()
        row.prop(context.scene, 'pathbox_sa_nodes')
        row = layout.row(align=True)
        props = row.operator("loader.sa_nodes_loader_operator")
        props.path = context.scene.pathbox_sa_nodes

        row = layout.row(align=True)
        props = row.operator("loader.ipl_paths_loader_operator")

def register():
    bpy.types.Scene.pathbox_sa_nodes = bpy.props.StringProperty \
    (
    name = "Root Path",
    default = r'E:\paths-visualizer\Vanilla\Compiled\SA',
    description = "Define the root path containing all nodes*.dat from GTA San Andreas",
    subtype = 'DIR_PATH'
    )

    bpy.utils.register_class(setup_scene_for_paths_op)
    bpy.utils.register_class(sa_nodes_loader_operator)
    bpy.utils.register_class(PathsUltimatumPanel)
    bpy.utils.register_class(ipl_paths_loader_operator)
    bpy.utils.register_class(path_mesh_viewer_panel)
    bpy.utils.register_class(ApplyVertCol)

def unregister():
    del bpy.types.Scene.pathbox_sa_nodes 

    bpy.utils.unregister_class(setup_scene_for_paths_op)
    bpy.utils.unregister_class(sa_nodes_loader_operator)
    bpy.utils.unregister_class(PathsUltimatumPanel)
    bpy.utils.unregister_class(ipl_paths_loader_operator)
    bpy.utils.unregister_class(path_mesh_viewer_panel)
    bpy.utils.unregister_class(ApplyVertCol)

if __name__ == "__main__":
    register()
