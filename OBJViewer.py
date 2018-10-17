import pygame
from pygame.constants import *
from math import *
from tkinter.filedialog import askopenfilename

width = 640
height = 480

def math_sin(x):
    return sin((x*pi)/180)

def math_cos(x):
    return cos((x*pi)/180)

class OBJ:
    def __init__(self, objpath):
        self.verts = []
        self.faces = []
        self.objdata = [[0,0,0],[0,0,0],[0,0,0]]
        for line in open(objpath, "r").readlines():
            if line.startswith("v "):
                v = line.replace(",", ".").split(" ")
                self.verts.append([float(v[1]), float(v[2]), float(v[3])])
            elif line.startswith("f "):
                f_tmp = line.split(" ")
                f = [face.split("/") for face in f_tmp]
                self.faces.append([int(f[1][0]), int(f[2][0]), int(f[3][0])])

def getScreenPos(pos, camdata):
    posX = (math_cos(camdata[1][1])*(pos[0]-camdata[0][0]))-(math_sin(camdata[1][1])*(pos[2]-camdata[0][2]))
    posZ = (math_cos(camdata[1][1])*(pos[2]-camdata[0][2]))+(math_sin(camdata[1][1])*(pos[0]-camdata[0][0]))
    posY = -((math_cos(camdata[1][0])*(pos[1]-camdata[0][1]))-(math_sin(camdata[1][0])*posZ))
    posZ = (math_cos(camdata[1][0])*posZ)+(math_sin(camdata[1][0])*(pos[1]-camdata[0][1]))
    if posZ > 0 and posX/posZ > -(width/height) and posX/posZ < (width/height) and posY/posZ > -1 and posY/posZ < 1:
        return [(width/2)+((posX/posZ)*(height/2)),(height/2)+((posY/posZ)*(height/2))]
    else:
        return None

pygame.init()
objpath = askopenfilename(title="Select an OBJ file", filetypes=(("OBJ Files","*.obj"),("All files","*.*")))
camdata = [[0,0,0],[0,0,0]]
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  0,   0, 255)
GREEN  = (  0, 255,   0)
RED    = (255,   0,   0)
L_GREY = (192, 192, 192)
M_GREY = (128, 128, 128)
D_GREY = ( 96,  96,  96)
size = [width, height]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("OBJ Viewer")
running = True
speed = 5
rotate = False
move = False
clock = pygame.time.Clock()
while running:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4:
                camdata[0][0] += speed*(math_sin(camdata[1][1])-(math_sin(camdata[1][1])*math_sin(camdata[1][0])))
                camdata[0][1] += speed*(math_sin(camdata[1][0]))
                camdata[0][2] += speed*(math_cos(camdata[1][1])-(math_cos(camdata[1][1])*math_sin(camdata[1][0])))
            elif e.button == 5:
                camdata[0][0] -= speed*(math_sin(camdata[1][1])-(math_sin(camdata[1][1])*math_sin(camdata[1][0])))
                camdata[0][1] -= speed*(math_sin(camdata[1][0]))
                camdata[0][2] -= speed*(math_cos(camdata[1][1])-(math_cos(camdata[1][1])*math_sin(camdata[1][0])))
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            mx, my = e.rel
            if rotate:
                camdata[1][0] -= my
                camdata[1][1] += mx
    screen.fill(BLACK)
    obj = OBJ(objpath)
    for face in obj.faces:
        poly = [getScreenPos(obj.verts[face[0]-1], camdata),
                getScreenPos(obj.verts[face[1]-1], camdata),
                getScreenPos(obj.verts[face[2]-1], camdata)]
        if not (poly[0] == None or poly[1] == None or poly[2] == None):
            pygame.draw.polygon(screen, M_GREY, poly, 1)
    pygame.display.flip()
pygame.quit()
