__author__ = 'Kai Kang'
import math
from OpenGL.GL import *
from OpenGL.GLUT import *

#---------------- class readfile
class readfile():
    def __init__(self,name):
        self.filename = name
    def getdata(self):
        f = open(self.filename)
        rotation_matrix = []
        for i in f:
            x,y,z = i.split(' ')
            a = [float(x),float(y),float(z)]
            rotation_matrix.append(a)
        return rotation_matrix

matrix = readfile("rotation.txt").getdata()                   #Read the File

#--------------------------- retrieve the rotation axis and angle
def trmatrix(matrix):
    tr_matrix = 0.0
    for i in range(len(matrix)):
        tr_matrix += matrix[i][i]
    return tr_matrix

angle = math.acos((trmatrix(matrix) - 1.0)/2.0)
axis = [(matrix[2][1] - matrix[1][2])/2/math.sin(angle), (matrix[0][2] - matrix[2][0])/2/math.sin(angle), (matrix[1][0] - matrix[0][1])/2/math.sin(angle)]
print 'angle =',angle*360/2/math.pi
print 'axis =',axis

#-------------------------- Drawing
SCREEN_SIZE = (640, 640)

def draw():
    glColor3f(1.0, 1.0, 1.0) #white
    glBegin(GL_POLYGON)
    glVertex3f(-1.2, -1.2, 0.0)
    glVertex3f(1.2, -1.2, 0.0)
    glVertex3f(1.2, 1.2, 0.0)
    glVertex3f(-1.2, 1.2, 0.0)
    glEnd()

    glColor3f(0.0, 1.0, 0.0) #green
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glEnd()

    glColor3f(0.0, 0.0, 1.0) #blue
    glBegin(GL_POLYGON)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glEnd()

    glColor3f(1.0, 0.0, 0.0) #red
    glBegin(GL_POLYGON)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, 0.0)
    glEnd()

    glColor3f(0.0, 0.0, 0.0) #black
    glBegin(GL_POLYGON)
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, -1.0, 0.0)
    glVertex3f(1.0, -1.0, 0.0)
    glEnd()

def drawFunc():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glPushMatrix()
    glRotate(angle*360/2/math.pi, axis[0], axis[1], axis[2]) #Rotation
    draw()
    glPopMatrix()

    glFlush()

def run():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
    glutInitWindowSize(*SCREEN_SIZE)
    glutCreateWindow(b"Kai Kang Homework 2")
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0)
    #Orthogonal views(Left, Right, Bottom, Top, Near, Far)
    glutDisplayFunc(drawFunc)
    glutMainLoop()

if __name__ == '__main__':
    run()