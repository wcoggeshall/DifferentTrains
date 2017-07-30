import pygame
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy
from OpenGL.GLU import *
import os
from matutils import *
from objutils import *



def vbo_obj(vnftTupleList):
    global vertices, normals, faceIDX, txcoords
    vertices, normals, faceIDX, txcoords = vnftTupleList
    global vboo
    pa = []
    for face in faceIDX:
        verts, norms, tcrds, matl = face
        gmat = getmtl()[matl]
        if 'texture_Kd' in gmat:
            glBindTexture(GL_TEXTURE_2D, gmat['texture_Kd'])
            print("glBindTexture called")
        else:
            glColor(gmat['Kd'])
            
        trueverts = [vertices[v-1] for v in verts]
        truenorms = [normals[n-1] for n in norms]
        truetcrds = [txcoords[t-1] for t in tcrds]
        #Desired format: [vx vy vz nx ny nz tu tv] x 3
        #Wait...Oh the last one is filled in with 0?
        for i in range(len(trueverts)):
            pa.append([trueverts[i] + truenorms[i] + truetcrds[i]])
    npa = numpy.array(pa,'f')
    vboo = vbo.VBO(npa)

#Normals are being interperted as coordinates somewhere

def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
    glMatrixMode(GL_MODELVIEW)
    gluPerspective(45, (display[0]/display[1]), 1, 50000.0)
    glEnable(GL_DEPTH_CLAMP)
    
    glEnable(GL_LIGHTING)
    globalAmbient = [0.2, 0.2, 0.2, 0.5]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, globalAmbient)
    glShadeModel(GL_FLAT)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (.2,.2,.2,.5))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, ( .8, .8, .8, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1,1, 1, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0,600,0))
    glClearColor(0,.6,.6,1)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    glTranslatef(0,0,-800)
    
    vbo_obj(readOBJ())
    vboo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glVertexPointer(3, GL_FLOAT, 32, vboo)
    glNormalPointer(GL_FLOAT, 32, vboo+12)
    glTexCoordPointer(2, GL_FLOAT, 32, vboo+24)


    #Game loop itself
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            C = 10
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_d]:
                glTranslatef(-1*C,0,0)
            if pressed[pygame.K_a]:
                glTranslatef(1*C,0,0)
            if pressed[pygame.K_w]:
                glTranslatef(0,0,-1*C)
            if pressed[pygame.K_s]:
                glTranslatef(0,0,1*C)
            if pressed[pygame.K_r]:
                glTranslatef(0,1*C,0)
            if pressed[pygame.K_f]:
                glTranslatef(0,-1*C,0)
            if pressed[pygame.K_q]:
                glRotatef(-10,0,1,0)
            if pressed[pygame.K_e]:
                glRotatef(10,0,1,0)
            if pressed[pygame.K_t]:
                glPushMatrix()
            if pressed[pygame.K_g]:
                glPopMatrix();
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glDrawArrays(GL_TRIANGLES, 0, len(faceIDX)*3)

        
        pygame.display.flip()
        pygame.time.wait(10)
        
main()
