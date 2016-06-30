__author__ = 'Kai Kang'
######################################################
#                                                    #
# This program is wrote by Kai Kang for CAD project. #
#                                                    #
######################################################
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

#Text
def glut_print( x,  y, z,  font,  text, r,  g , b , a):
    blending = False
    if glIsEnabled(GL_BLEND) :
        blending = True
    glColor3f(r, g, b)
    glRasterPos3f(x,y,z)
    for ch in text :
        glutBitmapCharacter( font ,  ord(ch) )
    if not blending :
        glDisable(GL_BLEND)

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

#class readfile
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

def cal_point(triangle, plane):
    threepoints = []
    ys = []
    thisline = []
    for i in range(3):
        threepoints.append(maping[0][triangle[i]-1])
        ys.append(maping[0][triangle[i]-1][1])
    #case 1 the triangle has nothing to do with the plane
    if max(ys) <= yset[plane + 1] or min(ys) >= yset[plane + 1]:
        return
    #for every line of a triangle
    for j in range(3):
        k1 = j
        k2 = j + 1
        if j == 2:
            k2 = 0
        #case 2 if the triangle has two points on the plane
        if yset[plane + 1] in ys:
            print 'some points on the plane'
            if ys[k1] == ys[k2] == yset[plane + 1]:
                thisline.append(threepoints[k1])
                thisline.append(threepoints[k2])
                print 'some line on the plane'
                return

        #case 3 this is the general case
        if ys[k1] < yset[plane + 1] < ys[k2] or ys[k2] < yset[plane + 1] < ys[k1]:
            t = (threepoints[k2][1] - yset[plane + 1])/(threepoints[k2][1] - threepoints[k1][1])
            ipoint = []
            for i in range(3):
                ipoint.append(threepoints[k2][i] + t * (threepoints[k1][i] - threepoints[k2][i]))
            thisline.append(ipoint)

    contour[plane].append(thisline)

#read the file here
maping = readfile("model.obj").getdata()

#find the max and the min of all ys
yall = []
for i in maping[0]:
    yall.append(i[1])
ymax = max(yall)
ymin = min(yall)
#input how many slices to cut into
print 'How many slices do you want to cut the model into?'
print 'Please input a number:'
number = input()
n = int(number)/1.0
#each slice
deltay = (ymax - ymin)/n
yset = []
for i in range(int(n)):
    yset.append(ymin + i*deltay)
#for the contour list
contour = []
for i in range(int(n-1)):
    contour.append([])

#get the contours
for p in range(int(n)-1):
    for f in maping[2]:
        triangle = []
        for i in range(3):
            triangle.append(f[i][0])
        cal_point(triangle, p)

#draw the contours
def draw():
    global n
    glDisable(GL_TEXTURE_2D) #Disable Texture in order to use color
    glColor3f(1.0, 1.0, 1.0) #white plane not sure this thing will work
    glLineWidth(2) #Line Width
    #want to draw some colorful lines
    cc = 1.0/n
    nn = 0
    for c in contour:
        glBegin(GL_LINES)
        glColor3f(nn*cc, 1.0, 1.0 - nn*cc) #change the color
        for i in c:
            glVertex3f(i[0][0], i[0][1], i[0][2])
            glVertex3f(i[1][0], i[1][1], i[1][2])
        glEnd()
        nn += 1
    #will not do any mapping

#this is for export the contours
def export_contours(contours):
    nnn = 1
    for c in contours:
        this_contour = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        for i in c:
            glVertex3f(i[0][0]/4.5 + 0.01, i[0][2]/4.5, 1.0)
            glVertex3f(i[1][0]/4.5 + 0.01, i[1][2]/4.5, 1.0)
        glEnd()
        filename = 'contour_' + str(nnn) + '.png'
        nnn += 1
        pygame.image.save(this_contour, filename)
        print("file {} has been saved".format(filename))
        pygame.display.flip()
    print 'All contour files has been saved successfully!'
    #have to add these here
    #dont know why
    pygame.init()
    glutInit()
    pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption('Kai Kang CAD Project')
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 25)
    gluLookAt(*H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #######################

#draw the botton
def draw2():
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_POLYGON)
    glVertex3f(2, 2.7, 5)
    glVertex3f(2, 3.5, 5)
    glVertex3f(3.5, 3.5, 5)
    glVertex3f(3.5, 2.7, 5)
    glEnd()

    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_POLYGON)
    glVertex3f(1.95, 2.65, 5)
    glVertex3f(1.95, 3.55, 5)
    glVertex3f(3.55, 3.55, 5)
    glVertex3f(3.55, 2.65, 5)
    glEnd()

    glut_print(2.1, 3.15, 5.1, GLUT_BITMAP_HELVETICA_18, 'Export the', 0, 0, 0, 1.0)
    glut_print(2.1, 2.85, 5.1, GLUT_BITMAP_HELVETICA_18, 'Contours', 0, 0, 0, 1.0)



def main():
    pygame.init()
    glutInit()
    pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption('Kai Kang CAD Project')
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 25)
    gluLookAt(*H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    while True:
        global m, M, x0, y0, x1, y1
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == MOUSEBUTTONDOWN:
                x0, y0 = pygame.mouse.get_pos()
                if 492 <= x0 <= 629 and 9 <= y0 <= 86:
                    export_contours(contour)
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

        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glMultTransposeMatrixf(m)
        draw()
        glPopMatrix()
        draw2()

        pygame.display.flip()

if __name__ == '__main__':
    main()