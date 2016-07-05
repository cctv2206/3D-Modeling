__author__ = 'Kai Kang'
import numpy
import pygame
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame.locals import *

SCREEN_SIZE = (640, 640)

M = [[1, 0, 0, 0],
     [0, 1, 0, 0],
     [0, 0, 1, 0],
     [0, 0, 0, 1]]
H = [12, -8, 5,
     0, 0, 0,
     0, 0, 1]

plane_y = 0.0

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

maping = readfile("model.obj").getdata()

#------------------do something to the y
y_all = []
for i in maping[0]:
    y_all.append(i[1])
ymax = max(y_all)
ymin = min(y_all)

n = 10.0
each = (ymax - ymin)/n
yset = []
for i in range(int(n)):
    yset.append(ymin + i*each)

contour = []
for i in range(int(n-1)):
    contour.append([])

def position(num):
    for i in range(int(n)-1):
        if (num >= yset[i]) and (num < yset[i + 1]):
            return i
    return int(n)-1

def getpoint(triangle, plane):
    threepoints = []
    ys = []
    thisline = []
    for i in range(3):
        threepoints.append(maping[0][triangle[i]-1])
        ys.append(maping[0][triangle[i]-1][1])
    #case 1
    if max(ys) <= yset[plane + 1] or min(ys) >= yset[plane + 1]:
        return

    for j in range(3):
        k1 = j
        k2 = j + 1
        if j == 2:
            k2 = 0
        #case 2
        if yset[plane + 1] in ys:
            if ys[k1] == ys[k2] == yset[plane + 1]:
                thisline.append(threepoints[k1])
                thisline.append(threepoints[k2])
                return

        #case 3
        if ys[k1] < yset[plane + 1] < ys[k2] or ys[k2] < yset[plane + 1] < ys[k1]:
            t = (threepoints[k2][1] - yset[plane + 1])/(threepoints[k2][1] - threepoints[k1][1])
            ipoint = []
            for i in range(3):
                ipoint.append(threepoints[k2][i] + t * (threepoints[k1][i] - threepoints[k2][i]))
            thisline.append(ipoint)

    contour[plane].append(thisline)

def draw_the_contour(triangle, the_y):

    threepoints = []
    ys = []
    thisline = []
    for i in range(3):
        threepoints.append(maping[0][triangle[i]-1])
        ys.append(maping[0][triangle[i]-1][1])
    #case 1
    if max(ys) <= the_y or min(ys) >= the_y:
        return

    for j in range(3):
        k1 = j
        k2 = j + 1
        if j == 2:
            k2 = 0
        #case 2
        if the_y in ys:
            if ys[k1] == ys[k2] == the_y:
                thisline.append(threepoints[k1])
                thisline.append(threepoints[k2])
                return

        #case 3
        if ys[k1] < the_y < ys[k2] or ys[k2] < the_y < ys[k1]:
            t = (threepoints[k2][1] - the_y)/(threepoints[k2][1] - threepoints[k1][1])
            ipoint = []
            for i in range(3):
                ipoint.append(threepoints[k2][i] + t * (threepoints[k1][i] - threepoints[k2][i]))
            thisline.append(ipoint)

    glLineWidth(5)
    glBegin(GL_LINES)
    glColor3f(0.0, 0.0, 0.0)
    for i in thisline:
        glVertex3f(i[0], the_y, i[2] + 1.5)
    glEnd()

for p in range(int(n)-1):
    for f in maping[2]:
        triangle = []
        for i in range(3):
            triangle.append(f[i][0])
        getpoint(triangle, p)

def draw():
    glDisable(GL_TEXTURE_2D) #Disable Texture in order to use color
    glLineWidth(2) #Line Width
    for c in contour:
        glBegin(GL_LINES)
        glColor3f(1.0, 1.0, 1.0)
        glEnd()

    glEnable(GL_TEXTURE_2D) #Enable Texture
    glBindTexture(GL_TEXTURE_2D, texture_id) #Bind a texture
    for f in maping[2]:
        glBegin(GL_POLYGON)
        for p in f:
            glTexCoord2f(maping[1][p[1]-1][0], maping[1][p[1]-1][1])
            glVertex3f(maping[0][p[0]-1][0], maping[0][p[0]-1][1], maping[0][p[0]-1][2])
        glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_plane():
    glColor3f(0.7, 0.6, 0.5)
    glBegin(GL_POLYGON)
    glVertex3f(-5.0, plane_y, -1.5)
    glVertex3f(-5.0, plane_y, 1.5)
    glVertex3f(5.0, plane_y, 1.5)
    glVertex3f(5.0, plane_y, -1.5)
    glEnd()

    for f in maping[2]:
        triangle = []
        for i in range(3):
            triangle.append(f[i][0])
        draw_the_contour(triangle, plane_y)

def save_contours(contours):
    nnn = 1
    for c in contours:
        this_contour = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | OPENGL | DOUBLEBUF)
        glClearColor(0.4, 0.4, 0.4, 0.4)
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2) #Line Width
        glBegin(GL_LINES)
        for i in c:
            glVertex3f(i[0][0]/4.5 + 0.01, i[0][2]/4.5, 1.0)
            glVertex3f(i[1][0]/4.5 + 0.01, i[1][2]/4.5, 1.0)
        glEnd()
        filename = str(nnn) + '.jpg'
        nnn += 1
        pygame.image.save(this_contour, filename)
        pygame.display.flip()
    print ('Done!')
    
    #----------------
    pygame.init()
    glutInit()
    pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption('Kai Kang')
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 25)
    gluLookAt(*H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #-----------------
    load_texture('model.jpg')

def main():
    global plane_y
    pygame.init()
    glutInit()
    pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption('Kai Kang')
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 25)
    gluLookAt(*H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    load_texture('model.jpg')
    save_contours(contour)

    while True:
        global m, M, x0, y0, x1, y1
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                x0, y0 = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONUP:
                M = m
        if pygame.key.get_pressed()[K_s]:
            if plane_y > ymin + 0.1:
                plane_y = plane_y - 0.1
        if pygame.key.get_pressed()[K_w]:
            if plane_y < ymax - 0.1:
                plane_y = plane_y + 0.1
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

        glClearColor(0.4, 0.4, 0.4, 0.4)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glMultTransposeMatrixf(m)
        draw()
        draw_plane()
        glPopMatrix()
        pygame.display.flip()

if __name__ == '__main__':
    main()