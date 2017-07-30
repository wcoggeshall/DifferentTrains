from matutils import *
import os

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

def getmtl():
    return mtl
