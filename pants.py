import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *

def readOBJ():
    of = open("C:\\Users\\walte\\Desktop\\t2.obj")
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
            elif vals[0] == 'f':
                face = []
                norms = []
                for v in vals[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    #norms.append(int(w[1]))
                    norms.append(int(w[2]))
                faces.append((face, norms))
    return vertices, normals, faces



def prep_OBJ():
    global dlist
    vertices, normals, faceIDX = readOBJ()
    print("Vertex list in prep:"+str(vertices))
    
    dlist = glGenLists(1)
    glNewList(dlist, GL_COMPILE) #A reusable, global commandlist stored in GL
    glFrontFace(GL_CCW)
    for face in faceIDX:
        verts, norms = face
        print("face:"+str(face))
        #glColor3f(1,1,1)
        glBegin(GL_QUADS)
        for i in range(len(verts)):
            if norms[i] > 0:
                glNormal3fv(normals[norms[i]-1])
                print("Normal="+str(normals[norms[i]-1]))
                #pass
            glVertex3fv(vertices[verts[i]-1])
            print("Vertex="+str(vertices[verts[i]-1]))
        glEnd()
    glEndList() #End the command list

def main():
    pygame.init()
    display = (800,800)
    pygame.display.set_mode(display, pygame.DOUBLEBUF|pygame.OPENGL)
    glMatrixMode(GL_MODELVIEW)
    gluPerspective(45, (display[0]/display[1]), 1, 50000.0)
    glEnable(GL_DEPTH_CLAMP)
    
    glEnable(GL_LIGHTING)
    globalAmbient = [0.5, 0.5, 0.5, 0.5]
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, globalAmbient)
    glShadeModel(GL_FLAT)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (-1.5,1,-4,1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, ( 0, 1, 0, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0,5,-2))
    #glClearColor(1,1,1,1)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    #glLoadIdentity()
    #glRotatef(90,0,1,0)
    prep_OBJ()

    #Game loop itself
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            C = 10
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_d]:
                glTranslatef(1*C,0,0)
            if pressed[pygame.K_a]:
                glTranslatef(-1*C,0,0)
            if pressed[pygame.K_w]:
                glTranslatef(0,0,-1*C)
            if pressed[pygame.K_s]:
                glTranslatef(0,0,1*C)
            if pressed[pygame.K_r]:
                glTranslatef(0,1*C,0)
            if pressed[pygame.K_f]:
                glTranslatef(0,-1*C,0)
            if pressed[pygame.K_q]:
                glRotatef(5,0,1,0)
            if pressed[pygame.K_e]:
                glRotatef(-5,0,1,0)
            if pressed[pygame.K_t]:
                glPushMatrix()
            if pressed[pygame.K_g]:
                glPopMatrix();
                
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #glRotatef(1,0,1,0)
        gluCylinder(gluNewQuadric(), 10, 20, 100, 10, 10)
        #gluSphere(gluNewQuadric(),100,32,8)
        
        glCallList(dlist)
        pygame.display.flip()
        pygame.time.wait(10)
        
main()
