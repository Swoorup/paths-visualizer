from OpenGL.GL import *
import OpenGL.GL.shaders
import bpy
import bmesh
from mathutils import *
from math import *
from .ui_constants import *

class LinkInfoHelper:
    gllistIndex = -1
    
    @staticmethod
    def create_display_list(context):
        ob = context.object
        if ob is None:
            return
        
        if bpy.context.active_object.mode != 'EDIT':
            return
            
        ob = context.edit_object
        bm = bmesh.from_edit_mesh(ob.data)
        index = glGenLists(1)
        
        glNewList(index, GL_COMPILE)
        
        for e in bm.edges:
            vecFrom = e.verts[0].co
            vecTo = e.verts[1].co
    
            middle = (vecTo + vecFrom) / 2.0
            
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
            
            glColor3f(0.0,0.0,0.0)
            glBegin(GL_TRIANGLE_STRIP)
            for i in arrow_vertices:
                vert = Vector(i)
                vert *= SCALE
                vert.rotate(eulerRot)
                vert += middle
                glVertex3f(*vert)      
            glEnd()
            
            # Lane Information
            glColor3f(0.0,0.0,1.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMLEFTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert += Vector((-1.0 * (j + 1), 0.0, 0.0)) #left
                    vert.rotate(eulerRot)
                    vert += middle
                    glVertex3f(*vert)      
                glEnd()
                
                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert.rotate(Euler((0.0, 0.0, radians(180.0))))
                    vert += Vector((-1.0 * (j + 1), 0.0, 0.0)) #left
                    vert.rotate(eulerRot)
                    vert += middle
                    glVertex3f(*vert)      
                glEnd()
            
            glColor3f(0.0,1.0,0.0)
            for j in range(e[bm.edges.layers.int[EDGE_NUMRIGHTLANES]]):
                glBegin(GL_LINES)
                for i in line_vertices:
                    vert = Vector(i)
                    vert = Vector((vert.x, vert.y  * (vecTo - vecFrom).length, vert.z)) # scale
                    vert += Vector((1.0 * (j + 1), 0.0, 0.0)) #left
                    vert.rotate(eulerRot)
                    vert += middle
                    glVertex3f(*vert)      
                glEnd()
                
                glBegin(GL_TRIANGLE_STRIP)
                for i in arrow_vertices:
                    vert = Vector(i)
                    vert *= SCALE
                    vert += Vector((1.0 * (j + 1), 0.0, 0.0)) #left
                    vert.rotate(eulerRot)
                    vert += middle
                    glVertex3f(*vert)      
                glEnd()
            """
            glBegin(GL_LINE_STRIP)
            glVertex3f(*(middle + v1))
            glVertex3f(*(middle))
            glVertex3f(*(middle + v2))
            glEnd()
            """
        glEndList()
        LinkInfoHelper.gllistIndex = index
        return index
    
    @staticmethod
    def delete_display_list():
        if LinkInfoHelper.gllistIndex != -1:
            glDeleteLists(LinkInfoHelper.gllistIndex, 1)
            LinkInfoHelper.gllistIndex = -1
    
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
            
        if LinkInfoHelper.gllistIndex == -1:
            LinkInfoHelper.gllistIndex = LinkInfoHelper.create_display_list(context)
        
        #LinkInfoHelper.delete_display_list()
        #LinkInfoHelper.create_display_list(context)
    
        # 50% alpha, 2 pixel width line
        #glEnable(GL_BLEND)
        glColor4f(1.0, 1.0, 1.0, 0.5)
        #glLineWidth(2)
        
        glPushMatrix()
        glScalef(*ob.scale)
        glTranslatef(*ob.location)
        glCallList(LinkInfoHelper.gllistIndex)
        glPopMatrix()
    
        # restore opengl defaults
        glLineWidth(1)
        glDisable(GL_BLEND)
        glColor4f(0.0, 0.0, 0.0, 1.0)
     
    @staticmethod
    def cleanup():
        LinkInfoHelper.delete_display_list()