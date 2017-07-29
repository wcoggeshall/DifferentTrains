import pygame
from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy
from OpenGL.GLU import *
import os

def MTL(filename):
    contents = {}
    matl = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        values = line.split()
        if not values: continue
        if values[0] == 'newmtl':
            matl = contents[values[1]] = {}
        elif matl is None:
            raise ValueError("mtl file doesn't start with newmtl stmt")
        elif values[0] == 'map_Kd':
            # load the texture referred to by this declaration
            matl[values[0]] = values[1]
            surf = pygame.image.load(matl['map_Kd'])
            image = pygame.image.tostring(surf, 'RGBA', 1)
            assert image is not None
            ix, iy = surf.get_rect().size
            texid = glGenTextures(1)
            matl['texture_Kd'] = texid
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            matl[values[0]] = list(map(float, values[1:]))
    return contents

def readOBJ():
    of = open("C:\\Users\\walte\\Desktop\\Trains\\t7.obj")
    of.seek(0)
    vertices = []
    normals = []
    faces = []
    texcoords = []
    material = None
    global mtl
    for line in of:
        vals = line.split()
        if vals == []:
            continue
        if vals[0]=='v':
            vertices.append(list(map(float,vals[1:4])))
        elif vals[0] ==  'vn':
            normals.append(list(map(float, vals[1:4])))
        elif vals[0] == 'vt':
            texcoords.append(list(map(float, vals[1:3])))
        elif vals[0] in ('usemtl', 'usemat'):
            material = vals[1]
        elif vals[0] == 'mtllib':
            mtl = MTL(os.getcwd() + str(vals[1])[1:])
        elif vals[0] == 'f':
            face = []
            norms = []
            tcoords = []
            for v in vals[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                if len(w) >= 2 and len(w[1]) > 0:
                   tcoords.append(int(w[1]))
                else:
                       tcoords.append(0)
                if len(w) >= 3 and len(w[2]) > 0:
                    norms.append(int(w[2]))
                else:
                    norms.append(0)
                faces.append((face, norms, tcoords, material))
    return vertices, normals, faces, texcoords


def vbo_obj():
    global vertices, normals, faceIDX, txcoords
    vertices, normals, faceIDX, txcoords = readOBJ()
    global vboo
    pa = []
    for face in faceIDX:
        verts, norms, tcrds, matl = face
        gmat = mtl[matl]
        if 'texture_Kd' in gmat:
            glBindTexture(GL_TEXTURE_2D, gmat['texture_Kd'])
            print("glBindTexture called")
        else:
            glColor(gmat['Kd'])
            
        trueverts = [vertices[v-1] for v in verts]
        truenorms = [normals[n-1] for n in norms]
        truetcrds = [txcoords[t-1] for t in tcrds]
        #Are txcoords references? no. Are tcrds?
        #Desired format: [vx vy vz nx ny nz tu tv] x 3 
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
    glLightfv(GL_LIGHT0, GL_DIFFUSE, ( .8, .8, .7, 1))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1,1, 1, 1))
    glLightfv(GL_LIGHT0, GL_POSITION, (0,600,0))
    glClearColor(0,.6,.6,1)
    glEnable(GL_LIGHT0)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)

    glTranslatef(0,0,-800)
    
    vbo_obj()
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
