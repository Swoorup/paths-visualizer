import bpy
import bmesh
from mathutils import *
from math import *
from .ui_constants import *
from bgl import *
from bpy.props import BoolProperty

class LinkInfoHelper:
    displayList = -1
    kd = None
    
    @staticmethod
    def draw_lane_info():
        context = bpy.context
        ob = context.object
        if ob is None:
            return
        
        ob = context.edit_object
        bm = bmesh.from_edit_mesh(ob.data)
        view_mat = context.space_data.region_3d.perspective_matrix
        ob_mat = context.active_object.matrix_world
        total_mat = view_mat * ob_mat
        
        for e in bm.edges:
            vecTo = e.verts[0].co # 0 is the target 
            vecFrom = e.verts[1].co   # 1 is the source
            
            viewportVert1 = total_mat * vecTo
            viewportVert2 = total_mat * vecFrom
            
            if viewportVert1.x < -1.0 or viewportVert1.y < -1.0 or viewportVert1.z < -1.0:
                continue
                
            if viewportVert1.x > 1.0 or viewportVert1.y > 1.0 or viewportVert1.z > 1.0:
                continue
                
            if viewportVert2.x < -1.0 or viewportVert2.y < -1.0 or viewportVert2.z < -1.0:
                continue
                
            if viewportVert2.x > 1.0 or viewportVert2.y > 1.0 or viewportVert2.z > 1.0:
                continue

            center = (vecTo + vecFrom) / 2.0
            
            v = vecTo - vecFrom
            v.normalize()
            
            # if vector is straight pointing up only on z axis ignore it
            if abs(v.x) < 0.0001 and abs(v.y) < 0.0001:
                continue
            
            vPerp1 = Vector((-v.y, v.x, 0.0))
            vPerp2 = Vector((v.y, -v.x, 0.0))
            
            v1 = (vPerp1 - v).normalized()
            v2 = (vPerp2 - v).normalized()
            
            arrow_vertices = (
                (-0.5,-1.0, 0.0 ),
                ( 0.0, 1.0, 0.0 ),
                ( 0.0, 0.0, 0.0 ),
                ( 0.5,-1.0, 0.0 ),
            )
            
            line_vertices = (
                (-0.5, 0.5, 0.0 ) ,     
                (-0.5, -0.5, 0.0 ),
                ( 0.5, -0.5, 0.0 ),
                ( 0.5, 0.5, 0.0 ) ,
            )
            
            SCALE = 1.0
 
            #TODO: Perform by matrix instead
            hAngle = 0
            try:
                hAngle = v.xy.angle_signed(Vector((0,1)))
            except ValueError:
                pass
            # rotate towards x = 0, to find out the signed angle 
            v.rotate(Euler((0.0,0.0,-hAngle)))
            
            vAngle = radians(90)
            try:
                vAngle = v.yz.angle_signed(v.yx)
            except ValueError:
                if v.yz.length == 0.00:
                    continue
                vAngle = v.yz.angle_signed(Vector((1,0)))
                pass
                
            eulerRot = Euler((vAngle, 0.0, hAngle))
            mat = eulerRot.to_matrix().to_4x4()
            mat.translation = center
            
            glColor3f(0.0,0.0,0.0)
            glBegin(GL_TRIANGLE_STRIP)
            for i in arrow_vertices:
                vert = Vector(i)
                vert *= SCALE
                vert = mat * vert
                glVertex3f(*vert)      
            glEnd()

            lane_width = e[bm.edges.layers.float[EDGE_WIDTH]]
            SCALE = 0.5
            # Lane Information
            glColor3f(0.0,0.0,1.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMLEFTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert.x -= 0.5
                    vert.x += -1 * (j + 1) - lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()
                
                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert.x += 0.5
                    vert.rotate(Euler((0.0, 0.0, radians(180.0))))
                    vert.x += -1 * (j + 1) - lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()
            
            glColor3f(0.0,1.0,0.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert.x += 0.5
                    vert.x += 1 * (j + 1) + lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()
                
                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert.x += 0.5
                    vert.x += 1 * (j + 1) + lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()

    @staticmethod
    def create_display_list():
        LinkInfoHelper.displayList = glGenLists(1)
        glNewList(LinkInfoHelper.displayList, GL_COMPILE)
        LinkInfoHelper.draw_lane_info()
        glEndList()
    
    @staticmethod
    def delete_display_list():
        if LinkInfoHelper.displayList != -1:
            glDeleteLists(LinkInfoHelper.displayList, 1)
            LinkInfoHelper.displayList = -1
    
    @staticmethod
    def draw_callback_px():
        context = bpy.context
        wm = context.window_manager
        if wm.mesh_layer_editable.bDisplayEdgeDirection == False:
            LinkInfoHelper.delete_display_list()            
            return
        
        ob = context.object
        if ob is None or \
                ob.type != 'MESH' or \
                ob.mode != 'EDIT' or \
                wm.mesh_layer_editable.currentObj != ob.name:
            LinkInfoHelper.delete_display_list()
            return
          
        #LinkInfoHelper.delete_display_list()
        #LinkInfoHelper.draw_lane_info()
        
        if LinkInfoHelper.displayList == -1:
            LinkInfoHelper.create_display_list()
        
        # 50% alpha, 2 pixel width line
        #glEnable(GL_BLEND)
        glColor4f(1.0, 1.0, 1.0, 0.5)
        #glLineWidth(2)
        
        glPushMatrix()
        glScalef(*ob.scale)
        glTranslatef(*ob.location)
        glCallList(LinkInfoHelper.displayList)
        glPopMatrix()

        # restore opengl defaults
        glLineWidth(1)
        glDisable(GL_BLEND)
        glColor4f(0.0, 0.0, 0.0, 1.0)
     
    @staticmethod
    def cleanup():
        LinkInfoHelper.delete_display_list()

class LinkHelper():
    def __init__(self):
        self.kd = None
        self.options = {}

    # create kd tree based scene acceleration structure
    def create_accl_struct(self, obj): #blender object
        del self.kd

        bm = bmesh.from_edit_mesh(obj.data)
        self.kd = kdtree.KDTree( len(bm.edges) )

        for i, e in enumerate (bm.edges):
            center = ( e.verts[0].co + e.verts[1].co ) / 2
            self.kd.insert(center, i)

        self.kd.balance()

    """
    obj: blender object to draw around the link helper
    region_3d: region of the currect scene
    """
    def draw(self, obj, region_3d): 
        if self.kd is None:
            self.create_accl_struct(obj) 

        view_mat = region_3d.view_matrix
        cam_pos = view_mat.inverted_safe().translation
        print("viewing from: ", cam_pos) 
        for (co, index, dist) in self.kd.find_range(cam_pos, 600):
#            print ("    ", co, index, dist)
            bm = bmesh.from_edit_mesh(obj.data)
            e = bm.edges[index]
            vecTo = e.verts[0].co # 0 is the target 
            vecFrom = e.verts[1].co   # 1 is the source
            
            center = co
            
            v = vecTo - vecFrom
            v.normalize()
            
            # if vector is straight pointing up only on z axis ignore it
            if abs(v.x) < 0.0001 and abs(v.y) < 0.0001:
                continue
            
            vPerp1 = Vector((-v.y, v.x, 0.0))
            vPerp2 = Vector((v.y, -v.x, 0.0))
            
            v1 = (vPerp1 - v).normalized()
            v2 = (vPerp2 - v).normalized()
            
            arrow_vertices = (
                (-0.5,-1.0, 0.0 ),
                ( 0.0, 1.0, 0.0 ),
                ( 0.0, 0.0, 0.0 ),
                ( 0.5,-1.0, 0.0 ),
            )
            
            line_vertices = (
                (-0.5, 0.5, 0.0 ) ,     
                (-0.5, -0.5, 0.0 ),
                ( 0.5, -0.5, 0.0 ),
                ( 0.5, 0.5, 0.0 ) ,
            )
            
            SCALE = 1.0
 
            #TODO: Perform by matrix instead
            hAngle = 0
            try:
                hAngle = v.xy.angle_signed(Vector((0,1)))
            except ValueError:
                pass
            # rotate towards x = 0, to find out the signed angle 
            v.rotate(Euler((0.0,0.0,-hAngle)))
            
            vAngle = radians(90)
            try:
                vAngle = v.yz.angle_signed(v.yx)
            except ValueError:
                if v.yz.length == 0.00:
                    continue
                vAngle = v.yz.angle_signed(Vector((1,0)))
                pass
                
            eulerRot = Euler((vAngle, 0.0, hAngle))
            mat = eulerRot.to_matrix().to_4x4()
            mat.translation = center
            
            if dist < 130:
                glColor3f(0.0,0.0,0.0)
                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()

            lane_width = e[bm.edges.layers.float[EDGE_WIDTH]]
            SCALE = 0.5
            # Lane Information
            glColor3f(0.0,0.0,1.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMLEFTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert.x -= 0.5
                    vert.x += -1 * (j + 1) - lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()
                
                if dist > 120: 
                    continue

                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert.x += 0.5
                    vert.rotate(Euler((0.0, 0.0, radians(180.0))))
                    vert.x += -1 * (j + 1) - lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()
            
            glColor3f(0.0,1.0,0.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert.x += 0.5
                    vert.x += 1 * (j + 1) + lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()
                
                if dist > 120: 
                    continue

                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert.x += 0.5
                    vert.x += 1 * (j + 1) + lane_width/2 #left
                    vert = mat * vert
                    glVertex3f(*vert)      
                glEnd()


    def __del__(self):
        print("Deleted Link Hlper", self)
        del self.kd

state = {}
state["frame_cb_hnd"] = -1
state["link_helper"] = None

def cb_frame_callback():
    context = bpy.context
    ob = context.edit_object
    if ob is None:
        return

    state["link_helper"].draw(ob, context.space_data.region_3d) 

    glLineWidth(1)
    glDisable(GL_BLEND)
    glColor4f(0.0, 0.0, 0.0, 1.0)

def cb_scene_callback(context):
    edit_obj = bpy.context.edit_object
    if edit_obj is not None and edit_obj.is_updated_data is True:
        print("Edited")
        state["link_helper"].create_accl_struct(edit_obj)

def setup():
    def boolDisplayLaneCallback(self, context):
        if (self.boolDisplayLane):
            if cb_scene_callback not in bpy.app.handlers.scene_update_post:
                bpy.app.handlers.scene_update_post.append(cb_scene_callback)
                state["frame_cb_hnd"] = bpy.types.SpaceView3D.draw_handler_add(cb_frame_callback, (), 'WINDOW', 'POST_VIEW')
        else:
            if cb_scene_callback in bpy.app.handlers.scene_update_post:
                bpy.app.handlers.scene_update_post.remove(cb_scene_callback)
                bpy.types.SpaceView3D.draw_handler_remove(state["frame_cb_hnd"], 'WINDOW')

    
    bpy.types.Scene.boolDisplayLane = BoolProperty(name="Enable or Disable", description="Should Display Lane Helper?", default=False, update=boolDisplayLaneCallback) 
    state["link_helper"] = LinkHelper()

def cleanup():
    if cb_scene_callback in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.remove(cb_scene_callback)
        bpy.types.SpaceView3D.draw_handler_remove(state["frame_cb_hnd"] , 'WINDOW')

    del bpy.types.Scene.boolDisplayLane
    del state["link_helper"]
