import pygame
from OpenGL.GL import *

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
