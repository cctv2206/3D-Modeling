__author__ = 'kk'
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

rotx = 0
roty = 0

def init():
    glClearColor(0.5, 0.5, 0.5, 0) #Gray Background

    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluPerspective(40, 1, 0.1, 10) # "Field of View" Angle (Deg), Aspect Ratio , Near Clip, Far Clip
    glMatrixMode(GL_MODELVIEW)

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

def draw():
    glColor3f(0.5, 1.0, 1.0) #Light Blue
    glBegin(GL_POLYGON)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glEnd()

    glColor3f(0.0, 1.0, 0.0) #green
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glEnd()

    glColor3f(0.0, 0.0, 1.0) #blue
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0) #red
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glEnd()

    glColor3f(1.0, 1.0, 0.0) #yellow
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glEnd()

    glColor3f(1.0, 0.0, 1.0) #purple
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glEnd()

    #--------Draw the three Axis
    glColor3f(0, 1, 1) #white
    glLineWidth(4) #Line Width
    glBegin(GL_LINES)
    glVertex3f(-1.4, 0.0, 0.0)
    glVertex3f(1.4, 0.0, 0.0)
    glVertex3f(0.0, -1.4, 0.0)
    glVertex3f(0.0, 1.4, 0.0)
    glVertex3f(0.0, 0.0, -1.4)
    glVertex3f(0.0, 0.0, 1.4)
    glEnd()
    glBegin(GL_POLYGON)
    glVertex3f(1.5, 0.0, 0.0)
    glVertex3f(1.3, 0.04, 0.0)
    glVertex3f(1.3, -0.04, 0.0)
    glEnd()
    glBegin(GL_POLYGON)
    glVertex3f(0.0, 1.5, 0.0)
    glVertex3f(0.04, 1.3, 0.0)
    glVertex3f(-0.04, 1.3, 0.0)
    glEnd()
    glBegin(GL_POLYGON)
    glVertex3f(0.0, 0.0, 1.5)
    glVertex3f(0.04, 0.0, 1.3)
    glVertex3f(-0.04, 0.0, 1.3)
    glEnd()
    glut_print(1.4, -0.15, 0.0, GLUT_BITMAP_HELVETICA_18, unichr(120), 0, 0, 0, 1.0)
    glut_print(-0.15, 1.4, 0.0, GLUT_BITMAP_HELVETICA_18, unichr(121), 0, 0, 0, 1.0)
    glut_print(-0.15, 0.0, 1.4, GLUT_BITMAP_HELVETICA_18, unichr(122), 0, 0, 0, 1.0)

def mouse(button,state,x,y):
    global beginx,beginy,rotate
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rotate = 1
        beginx = x
        beginy = y
    if button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        rotate = 0
    return

def motion(x,y):
    global rotx,roty,beginx,beginy,rotate
    if rotate:
        rotx = rotx + (y - beginy)
        roty = roty + (x - beginx)
        beginx = x
        beginy = y
        glutPostRedisplay()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() #Loads Global Matrix

    gluLookAt(5,0,0,   # Camera Position
    0,0,0,      # Point the Camera looks at
    0,1,0)      # the Up-Vector

    glRotated(roty,0,1,0)   #rotate y
    glRotated(rotx,1,0,0)   #rotate x

    draw()

    glutSwapBuffers()
    glFlush()
    return

glutInit('Homework 4 Kai Kang')
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(640, 640)
glutCreateWindow('Homework 4 Kai Kang')

glutDisplayFunc(display)
glutMouseFunc(mouse)
glutMotionFunc(motion)

init()
glutMainLoop()
