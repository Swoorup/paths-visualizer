import bpy
import bgl
import blf
import bmesh
from mathutils import *
from math import *

def draw_arrow_head(self, context, vecFrom, vecTo):
    ob = context.object
    if ob is None:
        return
    
    arrow = [
        [-1,-1],
        [0,0],
        [1,-1],
    ]
    
    middle = (Vector(vecTo) + Vector(vecFrom)) / 2.0
    
    v = Vector(vecTo) - Vector(vecFrom)
    v.normalize()
    
    vPerp1 = Vector((-v.y, v.x, 0.0))
    vPerp2 = Vector((v.y, -v.x, 0.0))
    
    v1 = (vPerp1 - v).normalized()
    v2 = (vPerp2 - v).normalized()
    
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(*(middle + v1))
    bgl.glVertex3f(*(middle))
    bgl.glVertex3f(*(middle + v2))
    bgl.glEnd()
    
    """
    direction = Vector(vecTo) - Vector(vecFrom)
    angle = direction.angle(Vector((1,0,0 )))
    
    # form a 2d rotation matrix
    mat = Matrix()
    mat.rotate((0,0,angle))
    
    # middle point
    
    
    bgl.glBegin(bgl.GL_LINE_STRIP)
    for v in arrow:
        xy = mat * Vector(v).to_3d()
        newPos = xy + middle
        bgl.glVertex3f(*newPos)
    bgl.glEnd()
    """

def draw_edge_direction(self, context):
    ob = context.object
    if ob is None:
        return
    
    if bpy.context.active_object.mode != 'EDIT':
        return
        
    obj = context.edit_object
    me = obj.data
    
    bm = bmesh.from_edit_mesh(me)
    
    for e in bm.edges:
        draw_arrow_head(self, context, e.verts[0].co, e.verts[1].co)
    
    
def draw_callback_px(self, context):

    ob = context.object
    if ob is None:
        return

    # 50% alpha, 2 pixel width line
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(1.0, 1.0, 1.0, 0.5)
    bgl.glLineWidth(2)
    
    #draw_arrow_head(self, context, [1,1,0], [0,10,0])
    draw_edge_direction(self, context)
    
    """
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex3f(*ob.matrix_world.translation)
    bgl.glVertex3f(*context.scene.cursor_location)
    bgl.glEnd()
    """

    # restore opengl defaults
    bgl.glLineWidth(1)
    bgl.glDisable(bgl.GL_BLEND)
    bgl.glColor4f(0.0, 0.0, 0.0, 1.0)


class ModalDrawOperator(bpy.types.Operator):
    """Draw a line with the mouse"""
    bl_idname = "view3d.modal_operator"
    bl_label = "Simple Modal View3D Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'RIGHTMOUSE', 'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle = bpy.types.SpaceView3D.draw_handler_add(draw_callback_px, args, 'WINDOW', 'POST_VIEW')

            self.mouse_path = []

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalDrawOperator)


def unregister():
    bpy.utils.unregister_class(ModalDrawOperator)

if __name__ == "__main__":
    register()

    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            bpy.ops.view3d.modal_operator({'area': area}, 'INVOKE_DEFAULT')
            break