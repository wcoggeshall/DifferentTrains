import pygame
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy
from OpenGL.GLU import *

def readOBJ():
    of = open("C:\\Users\\walte\\Desktop\\t4.obj")
    of.seek(0)
    vertices = []
    normals = []
    faces = []
    for line in of:
        vals = line.split()
        if vals == []:
            continue
        if vals[0]=='v':
            vertices.append(list(map(float,vals[1:4])))
        elif vals[0] ==  'vn':
            normals.append(list(map(float, vals[1:4])))
    of.seek(0)
    for line in of:
        vals = line.split()
        if vals == []: continue
        if vals[0] == 'f':
            face = []
            norms = []
            for v in vals[1:]:
                w = v.split('//')
                face.append(int(w[0]))
                norms.append(int(w[1]))
            faces.append((face, norms))
    return vertices, normals, faces


def vbo_obj():
    global vertices, normals, faceIDX
    vertices, normals, faceIDX = readOBJ()
    global vboo
    pa = []
    for face in faceIDX:
        verts, norms = face
        trueverts = [vertices[v-1] for v in verts]
        truenorms = [normals[n-1] for n in norms]
        #Desired format: [vx vy vz nx ny nz] x 3
        for i in range(len(trueverts)):
            pa.append([trueverts[i] + truenorms[i]])
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
    glLightfv(GL_LIGHT0, GL_DIFFUSE, ( .8, 0, 0, .7))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0,0.9, 0.5, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0,500,0))
    glClearColor(0,1,1,1)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)

    glTranslatef(0,0,-400)
    
    vbo_obj()
    vboo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, vboo)
    glNormalPointer(GL_FLOAT, 24, vboo+12)


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
