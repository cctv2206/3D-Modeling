__author__ = 'kk'
#----------------------- Import Functions & Modules -------------------------
import pygame
from pygame.locals import *
from sys import exit
import math

#----------------class readfile
class readfile():
    def __init__(self,name):
        self.filename = name
    def getdata(self):
        f = open(self.filename)
        list_point = []
        for i in f:
            x,y = i.split(',')
            a = [float(x),float(y)]
            list_point.append(a)
        return list_point

pointlist = readfile("p1.txt").getdata()                   #Read the File

#----------------------- Constant Definition ----------------------------------
SCREEN = (640, 640)                                                     # Window Size
CANVAS = (640, 640)                                                     # Canvas Size
CANVAS_BACKGROUND = (190, 190, 190)                                     # Default color for a Surface

#----------------------------Define Functions -------------------------------------
def draw_axis(canvas):
    pygame.draw.line(canvas, (100, 100, 100), (20, 320), (620,320), 3)   # x-axis
    pygame.draw.line(canvas, (100, 100, 100), (320, 20), (320,620), 3)   # y-axis
    #arrow x
    pygame.draw.line(canvas, (100, 100, 100), (620,320), (607,313), 3)
    pygame.draw.line(canvas, (100, 100, 100), (620,320), (607,327), 3)
    #arrow y
    pygame.draw.line(canvas, (100, 100, 100), (320,20), (313,30), 3)
    pygame.draw.line(canvas, (100, 100, 100), (320,20), (327,30), 3)
    #Draw line function (Surface, Color, Previous Point, Next Point, Size)

    pygame.draw.line(canvas, (0,0,0), (600,316),(600,324), 4)  # (1000,0) point
    pygame.draw.line(canvas, (0,0,0), (40,316),(40,324), 4)  # (-1000,0) point
    pygame.draw.line(canvas, (0,0,0), (316,40),(324,40), 4)  # (0,1000) point
    pygame.draw.line(canvas, (0,0,0), (316,600),(324,600), 4)  # (0,-1000) point

    font = pygame.font.Font(None,25)     # font
    # (1000,0)   (0,1000)
    text = font.render("1000",0,(0,0,0))
    textpos = text.get_rect()
    textpos.center = (600,340)
    canvas.blit(text,textpos)
    textpos.center = (348,40)
    canvas.blit(text,textpos)
    # (-1000,0)  (0,-1000)
    text = font.render("-1000",0,(0,0,0))
    textpos = text.get_rect()
    textpos.center = (40,340)
    canvas.blit(text,textpos)
    textpos.center = (351,600)
    canvas.blit(text,textpos)

def draw_points(canvas):
    for i in range(len(pointlist)):
        x = int(320 + pointlist[i][0]*0.28)
        y = int(320 - pointlist[i][1]*0.28)
        pygame.draw.circle(canvas, (254,117,5), (x,y), 4, 4)

def draw_circle(canvas):
    #find the radius
    radius = []
    for i in range(len(pointlist)):
        radius.append(math.sqrt(pointlist[i][0]**2+pointlist[i][1]**2))
    radius.sort()
    if len(radius)%2 == 0:
        r = radius[(len(radius)-1)/2]
    else:
        r = radius[len(radius)/2]
    pygame.draw.circle(canvas, (5,154,255), (320,320), int(r*0.28)+2, 2)

    pointsnumber = str(len(pointlist)) + '  Points'
    font = pygame.font.Font(None,30)     # font
    text = font.render(pointsnumber,0,(0,0,0))
    textpos = text.get_rect()
    textpos.center = (60,30)
    canvas.blit(text,textpos)

#------------------------------ Main Function -------------------------------------
def main():
    pygame.init()      #Initialize Pygame
    screen = pygame.display.set_mode(SCREEN, 0, 32)            # Initialize a window
    pygame.display.set_caption("Kai Kang Problem 1")                        # Window title
    canvas = pygame.Surface(CANVAS)                              # Initialize a Surface object
    canvas.fill(CANVAS_BACKGROUND)                               # Fill a Surface object with default color

    print draw_circle(canvas)
    while True:                                                                    #Main Loop
        for event in pygame.event.get():                               #Events Handling
            if event.type == QUIT:
                exit()

        draw_axis(canvas)                                                          #Call Draw Functions 1
        draw_points(canvas)
        draw_circle(canvas)

        screen.blit(canvas,(0,0))                                   #BLock Image Transfer
        #blit(Surface, Coordinates)

        pygame.display.update()                                          #Refresh, Redraw the screen

if __name__ == '__main__':
    main()
