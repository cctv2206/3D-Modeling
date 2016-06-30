__author__ = 'kk'
from OpenGL.GLUT import *
from math import *
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

SCREEN_SIZE = (640, 640)

M = [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
H = [0, 0, 15,
     0, 0, 0,
     0, 1, 0]

def load_texture(texture_path):
    global texture_id
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, 'RGB', True)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    width, height = texture_surface.get_rect().size
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE, texture_data)

def set_up_light(name, position, color):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    light_ambient =  color
    light_diffuse =  color
    light_specular = color

    light_position = position

    glLightfv(name, GL_AMBIENT, light_ambient)
    glLightfv(name, GL_DIFFUSE, light_diffuse)
    glLightfv(name, GL_SPECULAR, light_specular)
    glLightfv(name, GL_POSITION, light_position)
    glEnable(name)
    glPopMatrix()

#---------------- class readfile
class readfile():
    def __init__(self,name):
        self.filename = name
    def getdata(self):
        f = open(self.filename)
        mapingdata = [[], [], []]
        for i in f:
            data = i.split(' ')
            if data[0] == 'v':
                a, x, y, z = data
                a = [float(x),float(y),float(z)]
                mapingdata[0].append(a)
            if data[0] == 'vt':
                a, x, y = data
                a = [float(x), float(y)]
                mapingdata[1].append(a)
            if data[0] == 'f':
                a, x, y, z = data
                x1 = x.split('/')
                y1 = y.split('/')
                z1 = z.split('/')
                a = [[int(x1[0]), int(x1[1])], [int(y1[0]), int(y1[1])], [int(z1[0]), int(z1[1])]]
                mapingdata[2].append(a)
        return mapingdata

maping = readfile("model.obj").getdata()     #Read the Fil

def draw():
    glEnable(GL_TEXTURE_2D) #Enable Texture
    glBindTexture(GL_TEXTURE_2D, texture_id) #Bind a texture
    for f in maping[2]:
        glBegin(GL_POLYGON)
        for p in f:
            glTexCoord2f(maping[1][p[1]-1][0], maping[1][p[1]-1][1])
            glVertex3f(maping[0][p[0]-1][0], maping[0][p[0]-1][1], maping[0][p[0]-1][2])
        glEnd()

def main():
    pygame.init()
    glutInit()
    pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption('Kai Kang Homework 5')
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 25)
    gluLookAt(*H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_LIGHTING)   # enable lighting
    position = [-2, 2, 2, 1]
    color = [1, 1, 1, 0]
    set_up_light(GL_LIGHT0, position, color)  #set up light

    load_texture('model.jpg')

    while True:
        global m, M, x0, y0, x1, y1
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                x0, y0 = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                M = m

        m = M
        if pygame.mouse.get_pressed()[0]:
            x1, y1 = pygame.mouse.get_pos()
            xd, yd = x1 - x0, y1 - y0
            ax = yd/300.
            ay = xd/300.
            rx = [[1, 0, 0, 0],
                  [0, cos(ax), -sin(ax), 0],
                  [0, sin(ax), cos(ax), 0],
                  [0, 0, 0, 1]]
            ry = [[cos(ay), 0, sin(ay), 0],
                  [0, 1, 0, 0],
                  [-sin(ay), 0, cos(ay), 0],
                  [0, 0, 0, 1]]
            rxy = numpy.dot(rx, ry)
            m = numpy.dot(rxy, numpy.reshape(M, (4, -1)))
            m = list(numpy.reshape(m, (1, -1))[0])

        glClearColor(0.3, 0.3, 0.3, 0.3)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glMultTransposeMatrixf(m)
        draw()
        glPopMatrix()

        pygame.display.flip()

if __name__ == '__main__':
    main()