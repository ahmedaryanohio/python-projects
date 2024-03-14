import pygame
from sys import exit

import math

pygame.init()
screen = pygame.display.set_mode((750,500))
pygame.display.set_caption("sigma window")
clock = pygame.time.Clock()

uptime = 0

screenwidth, screenheight = 750, 500

midpoint = (screenwidth/2, screenheight/2, 0)

zdecay = 180

arrows, screens = [], []

class Vector3():
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def xyz(self):
        return self.x, self.y, self.z
    
class CFrame():
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation
    
    def position(self):
        return self.position
    
    def rotation(self):
        return self.rotation
    
class Triangle():
    def __init__(self, point1, point2, point3):
        self.point1 = point1
        self.point2 = point2
        self.point3 = point3

    def points(self):
        return self.point1, self.point2, self.point3
    
    def rep(self, func, arg):
        self.point1 = func(self.point1, arg)
        self.point2 = func(self.point2, arg)
        self.point3 = func(self.point3, arg)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, color, position, dirs, size, skewx, skewy, squashx, squashy, squashz, usx, usy, usz, uskx, usky):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.position = position
        self.dirs = dirs
        self.size = size
        self.spfx = [squashx, squashy, squashz, skewx, skewy]
        self.uspfx = [usx, usy, usz, uskx, usky]

class Screen(pygame.sprite.Sprite):
    def __init__(self, position, scroll, direction, parentdirection):
        self.position = position
        self.scroll = scroll
        self.direction = direction
        self.parentdirection = parentdirection

def sumt(tuple1, tuple2):
    return [a + b for a, b in zip(tuple1, tuple2)]

def rasterize(xyz1, xyz2):
    xy = sumt(xyz1, xyz2)
    xy = sumt(xy, (-midpoint[0],-midpoint[1],0))
    zpos = (xy[2]/zdecay)+1
    xy = (xy[0]/zpos,xy[1]/zpos)
    xy = sumt(xy, midpoint)
    return(xy)

def translatedirection(position, direction):
    xydir, xzdir, yzdir = math.radians(direction[0]+180), math.radians(direction[1]), math.radians(direction[2])
    translatedir  = (math.sin(xydir)*position[0] + math.cos(xydir)*position[1], math.sin(xydir)*position[1] - math.cos(xydir)*position[0], position[2])
    translatedir = (math.sin(xzdir)*translatedir[0] + math.cos(xzdir)*translatedir[2], translatedir[1], math.sin(xzdir)*translatedir[2] - math.cos(xzdir)*translatedir[0])
    translatedir = (translatedir[0], math.sin(yzdir)*translatedir[1] + math.cos(yzdir)*translatedir[2], math.sin(yzdir)*translatedir[2] - math.cos(yzdir)*translatedir[1])
    return translatedir

def uspfxd(point, uspfx):
    xyz = point[0:3]
    newpoint = [v3p * fx for v3p, fx in zip(xyz, uspfx)]
    newpoint = (newpoint[0] + (newpoint[1]*uspfx[3]),newpoint[1] + (newpoint[0]*uspfx[4]),newpoint[2])
    return newpoint

def screenfxify(point, SCREEN):
    point = sumt(point, SCREEN.position)
    point = sumt(point, SCREEN.scroll)
    return point

def triangle(point1, point2, point3, xyz, color, direction, uspfx, SCREEN):
    nmp = sumt(midpoint, xyz)
    np1, np2, np3 = translatedirection(point1, direction), translatedirection(point2, direction), translatedirection(point3, direction)
    np1, np2, np3 = uspfxd(np1, uspfx), uspfxd(np2, uspfx), uspfxd(np3, uspfx)
    np1, np2, np3 = screenfxify(np1, SCREEN), screenfxify(np2, SCREEN), screenfxify(np3, SCREEN)
    pygame.draw.polygon(screen, color, (rasterize(nmp, np1), rasterize(nmp, np2), rasterize(nmp, np3)))

def rewriteoffset(xyz,size,dirs,point1,point2,point3,color,spfx,uspfx,SCREEN):
    sizem = size * 0.01
    p1, p2, p3 = [point*sizem for point in point1], [point*sizem for point in point2], [point*sizem for point in point3]
    p1, p2, p3 = [point*fx for point, fx in zip(point1, spfx)], [point*fx for point, fx in zip(point2, spfx)], [point*fx for point, fx in zip(point3, spfx)]
    p1 = (p1[0]+(p1[1]*spfx[3]), p1[1]+(p1[0]*spfx[4]), p1[2])
    p2 = (p2[0]+(p2[1]*spfx[3]), p2[1]+(p2[0]*spfx[4]), p2[2])
    p3 = (p3[0]+(p3[1]*spfx[3]), p3[1]+(p3[0]*spfx[4]), p3[2])
    triangle(p1, p2, p3, xyz, color, dirs, uspfx, SCREEN)

def arrow(xyz, dirs, size, color, spfx, uspfx, SCREEN):
    rewriteoffset(xyz,size,dirs,(-7,-27,0),(7,-27,0),(7,-4,0),color,spfx,uspfx,SCREEN)
    rewriteoffset(xyz,size,dirs,(-7,-27,0),(-7,-4,0),(7,-4,0),color,spfx,uspfx,SCREEN)
    rewriteoffset(xyz,size,dirs,(7,-4,0),(31,-4,0),(19,-16,0),color,spfx,uspfx,SCREEN)
    rewriteoffset(xyz,size,dirs,(-7,-4,0),(-31,-4,0),(-19,-16,0),color,spfx,uspfx,SCREEN)
    rewriteoffset(xyz,size,dirs,(-31,-4,0),(31,-4,0),(0,27,0),color,spfx,uspfx,SCREEN)

arr = Arrow([150,150,150], [0, 0, 0], [90, 90, 90], 100, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0)

screenp = Screen([0,0,0],[0,0,0],[0,0,0],[0,0,0])

arrows.append(arr)
screens.append(screenp)

while True:

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0,0,screenwidth,screenheight))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for SCREEN in screens:
        for ARROW in arrows:
            arrow(ARROW.position, ARROW.dirs, ARROW.size, ARROW.color, ARROW.spfx, ARROW.uspfx,SCREEN)

    screens[0].scroll[0] = math.sin(uptime/40)*100
    arrows[0].dirs[1] = uptime

    pygame.display.update()
    clock.tick(60)

    uptime+=clock.tick(1000)