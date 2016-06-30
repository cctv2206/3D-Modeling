from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame, math
from pygame.locals import *

SCREEN_SIZE = (640, 640)

H = [0, 0, 5,
     0, 0, 0,
     0, 1, 0]

# Multiply
def vectmult(num, vect):
    return [num*vect[0], num*vect[1]]
# Sum
def twovectsum(a, b):
    return [a[0] + b[0], a[1] + b[1]]
def threevectsum(a, b, c):
    return[a[0] + b[0] + c[0], a[1] + b[1] + c[1]]
def fourvectsum(a, b, c, d):
    return[a[0] + b[0] + c[0] + d[0], a[1] + b[1] + c[1] + d[1]]


angle = 70
angle1 = angle
deg2rad = math.pi/180.0

def compute(angle):
    deg2rad = math.pi/180.0
    anglerad = angle * deg2rad
    #------------------- compute the 4 control points
    cos = math.cos(math.pi - anglerad)
    sin = math.sin(anglerad)

    global point0, point1, point2, point3, a, b, c, d, points, at3, bt2, ct, n
    point0 = [cos, -sin]
    point3 = [cos, sin]
    x = (-4.0 - cos)/3.0
    y = -(cos/sin) * (x - cos) + sin
    point2 = [x, y]
    point1 = [x, -y]
    points = [point0, point1, point2, point3]

    #-----------------------compute a,b,c,d
    a = fourvectsum(vectmult(-1,point0), vectmult(3,point1), vectmult(-3,point2), point3)
    b = threevectsum(vectmult(3,point0), vectmult(-6,point1), vectmult(3,point2))
    c = twovectsum(vectmult(-3,point0), vectmult(3,point1))
    d = point0

    #-----------------------compute something
    n = 100
    t = 1.0/n
    at3 = vectmult(t*t*t,a)
    bt2 = vectmult(t*t,b)
    ct = vectmult(t,c)

#text
def glut_print( x,  y,  font,  text, r,  g , b , a):
    blending = False
    if glIsEnabled(GL_BLEND) :
        blending = True
    #glEnable(GL_BLEND)
    glColor3f(0.0, 0.0, 0.0)
    glRasterPos2f(x,y)
    for ch in text :
        #glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )
        glutBitmapCharacter( font ,  ord(ch) )
    if not blending :
        glDisable(GL_BLEND)

#bezier curve
def draw_bezier():
    point = d
    d1point = threevectsum(at3,bt2,ct)
    d2point = twovectsum(vectmult(6,at3),vectmult(2,bt2))
    d3point = vectmult(6,at3)

    glColor3f(0, 1.0, 0) #green
    glLineWidth(4)
    glBegin(GL_LINE_STRIP)
    for i in range(n):
        point_next = twovectsum(point, d1point)
        glVertex3f(point[0], point[1], 0.0)
        glVertex3f(point_next[0], point_next[1], 0.0)
        d1point = twovectsum(d1point, d2point)
        d2point = twovectsum(d2point, d3point)
        point = point_next
    glEnd()

#draw lots of things
def draw(angle):
    #---------------draw background
    glColor3f(1.0, 1.0, 1.0) #white
    glBegin(GL_POLYGON)
    glVertex3f(-2, -2, 0.0)
    glVertex3f(2, -2, 0.0)
    glVertex3f(2, 2, 0.0)
    glVertex3f(-2, 2, 0.0)
    glEnd()

    '''GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP,
    GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN,
    GL_QUADS, GL_QUAD_STRIP, GL_POLYGON'''

    #--------Draw the two Axis
    glColor3f(0, 0, 0) #black
    glLineWidth(4) #Line Width
    glBegin(GL_LINES)
    glVertex3f(-1.4, 0.0, 0.0)
    glVertex3f(1.4, 0.0, 0.0)
    glVertex3f(0.0, -1.4, 0.0)
    glVertex3f(0.0, 1.4, 0.0)
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

    #-------------------arc
    glColor3f(1.0, 0, 0) #red
    glLineWidth(4) #Line Width
    glBegin(GL_LINE_STRIP)
    for i in range(360-int(angle) *2 + 1):
        deginrad = (angle - 180.0 +i) * deg2rad
        glVertex3f(math.cos(deginrad),math.sin(deginrad),0.0)
    glEnd()

    #line1&2
    linepoint = [1.2 * point3[0],1.2 * point3[1]]
    glColor3f(0, 0, 0) #black
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(linepoint[0],linepoint[1], 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(linepoint[0],-linepoint[1], 0.0)
    glEnd()

    #lines
    glColor3f(0.0, 0.0, 1.0) #blue
    glLineWidth(1) #Line Width
    glBegin(GL_LINE_STRIP)
    glVertex3f(point3[0], point3[1], 0.0)
    glVertex3f(point2[0], point2[1], 0.0)
    glVertex3f(point1[0], point1[1], 0.0)
    glVertex3f(point0[0], point0[1], 0.0)
    glEnd()

    #bezier curve
    draw_bezier()

    #-------------------control points
    glColor3f(0, 0, 0) #black
    glLineWidth(4)
    glBegin(GL_LINES)
    for i in points:
        glVertex3f(i[0]-0.05, i[1], 0.0)
        glVertex3f(i[0]+0.05, i[1], 0.0)
        glVertex3f(i[0], i[1]-0.05, 0.0)
        glVertex3f(i[0], i[1]+0.05, 0.0)
    glEnd()
    j = 0
    for i in points:
        glut_print(i[0]-0.15, i[1]-0.1, GLUT_BITMAP_HELVETICA_18, 'P', 0.0, 1.0, 1.0, 1.0)
        glut_print(i[0]-0.1, i[1]-0.12, GLUT_BITMAP_HELVETICA_12, unichr(48 + j), 0.0, 1.0, 1.0, 1.0)
        j += 1
    glut_print(1.4, -0.15, GLUT_BITMAP_HELVETICA_18, unichr(120), 0.0, 1.0, 1.0, 1.0)
    glut_print(-0.15, 1.4, GLUT_BITMAP_HELVETICA_18, unichr(121), 0.0, 1.0, 1.0, 1.0)
    glut_print(0.7, -1, GLUT_BITMAP_HELVETICA_18, 'Use A and D key to', 0.0, 1.0, 1.0, 1.0)
    glut_print(0.7, -1.1, GLUT_BITMAP_HELVETICA_18, 'adjust the angle', 0.0, 1.0, 1.0, 1.0)
    #glutSwapBuffers()

def drawFunc(angle):
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    #glPushMatrix()
    draw(angle)
    #glPopMatrix()
    glFlush()

def move(angle):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

 #-----------------Keyboard----------------------------------------
        if pygame.key.get_pressed()[K_a]:
            #rotation -=5
            if angle >1:
                angle -=1
        if pygame.key.get_pressed()[K_d]:
            #rotation +=5
            if angle < 179:
                angle +=1
        #angle changed
        compute(angle)
  #--------------------------------------------------------------------
        drawFunc(angle)
        pygame.display.flip()

def main():
    compute(angle)
    glutInit()
    pygame.init()    
    screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE|OPENGL|DOUBLEBUF)
    pygame.display.set_caption("Homework 3 - Kai Kang")
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_ALWAYS)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40, 1, 0.1, 10)
    gluLookAt(*H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #moving
    move(angle)

if __name__ == '__main__':
    main()