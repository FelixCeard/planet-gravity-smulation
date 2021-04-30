import pygame
from pygame import gfxdraw, Color
import sys
import uuid
import math
import random

pygame.init()

SCREEN_SIZE = (1920, 1080)
SCREEN_HALF_SIZE = (1920/2, 1080/2)
screen = pygame.display.set_mode(SCREEN_SIZE)

TRAILS = []


G = 6.67430*(10**(-11))

def alpha(color):
    # print(color, '->', (color[0], color[1], color[2], int(0.2*255)))
    return Color(color[0], color[1], color[2], int(0*255))
# init the trails

def calc_forces(LIST_OF_BODYS):
    for Body in LIST_OF_BODYS:
        Velocity_to_change = (0, 0)
        for comp_body in LIST_OF_BODYS:
            if Body.id != comp_body.id:
                # different bodys
                inner = math.pow((Body.pos[0] - comp_body.pos[0]), 2) + math.pow((Body.pos[1] - comp_body.pos[1]),2)
                if (inner < 0):
                    print(inner)
                distance = math.sqrt(inner)
                if distance == 0:
                    distance = 1
                F = G * (Body.weight * comp_body.weight) / (distance**2)
                d = (comp_body.pos[0] - Body.pos[0], comp_body.pos[1] - Body.pos[1]) # direction vector
                dm = max(abs(d[0]), abs(d[1]))
                if dm == 0:
                    dm = 1
                dnorm = (d[0]/dm, d[1]/dm) # normalized between 0 and 1
                F = F/2
                dnorm = (d[0] * F, d[1] * F) # not the correct math but fuck you
                Velocity_to_change = (Velocity_to_change[0] + dnorm[0], Velocity_to_change[1] + dnorm[1])
            else:
                continue
        Body.velocity = (Velocity_to_change[0] + Body.velocity[0], Velocity_to_change[1] + Body.velocity[1])

def get_center(LIST_OF_BODYS):
    c = (0, 0)
    for Body in LIST_OF_BODYS:
        c = (c[0] + Body.pos[0], c[1] + Body.pos[1])
    c = (c[0]/len(LIST_OF_BODYS), c[1]/len(LIST_OF_BODYS))
    return c
    # print('center in position', c)

def hextofloats(h):
    '''Takes a hex rgb string (e.g. #ffffff) and returns an RGB tuple (float, float, float).'''
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))

class Body:
    def __init__(self, start_pos, weight, a = 1, size = 5, vel = (0,0),color = (255, 255, 200)):
        self.pos = start_pos
        self.weight = weight
        self.size = size
        self.color = color
        self.velocity = vel
        self.velocity_multiplayer = a
        self.id = uuid.uuid4()
    def draw(self, scr=screen):
        self.tick()
        # pygame.draw.circle(scr, self.color, self.pos, self.size)
        # print('position is', int(self.pos[0]+ SCREEN_HALF_SIZE[0]/2), int(self.pos[1] + SCREEN_HALF_SIZE[1]/2))
        gfxdraw.filled_circle(scr, int(self.pos[0]+ SCREEN_HALF_SIZE[0]), int(self.pos[1] + SCREEN_HALF_SIZE[1]), self.size, self.color)
        # exit()
    def tick(self):
        self.pos = (self.pos[0] + self.velocity[0] * self.velocity_multiplayer, self.pos[1] + self.velocity[1] * self.velocity_multiplayer)


def distance_from_center(p):
    return math.sqrt(math.pow((SCREEN_SIZE[0]/2)-p[0], 2) + math.pow((SCREEN_SIZE[1]/2)-p[1], 2))

def diff(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


def mult(p1, a):
    return (p1[0] *a, p1[1] *a)


def reshape_everything(LIST_OF_BODYS, r, trails):
    for body in LIST_OF_BODYS:
        diff_from_center = diff(body.pos, (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
        # print((1-r))
        np = (body.pos[0] - diff_from_center[0]*(1-r), body.pos[1] - diff_from_center[1]*(1-r))
        # print(body.pos)
        body.pos = np
    for t in trails:
        for i in range(len(t)):
            diff_to_center = diff(t[i], (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
            # print(diff_to_center)
            t[i] = (t[i][0] - diff_from_center[0]*(1-r), t[i][1] - diff_from_center[1]*(1-r))
def fucking_go_auto_zoom(LIST_OF_BODYS, TRAILS):
    for b in LIST_OF_BODYS:
        p =  is_sus(b.pos)
        if (p != 0):
            # found a body outside the perimeter
            if p == 1: # left 
                d = 0.25*SCREEN_SIZE[0] - b.pos[0]
                r = (0.25*SCREEN_SIZE[0])/(0.25*SCREEN_SIZE[0]+d)
            if p == 2: # top
                d = 0.25*SCREEN_SIZE[1] - b.pos[1]
                r = (0.25*SCREEN_SIZE[1])/(0.25*SCREEN_SIZE[1]+d)
            if p == 3: # right 
                d = b.pos[0] - 0.75*SCREEN_SIZE[0]
                r = (0.75*SCREEN_SIZE[0])/(0.75*SCREEN_SIZE[0]+d)
            if p == 4: # bottom
                d = b.pos[1] - 0.75*SCREEN_SIZE[1] 
                r = (0.75*SCREEN_SIZE[1])/(0.75*SCREEN_SIZE[1]+d)
            # r = 1/r
            return reshape_everything(LIST_OF_BODYS, r, TRAILS)
    return False

def is_sus(p1):
    if p1[0] < -1*SCREEN_HALF_SIZE[0]/2:
        return 1
    if p1[1] < -1*SCREEN_HALF_SIZE[1]/2:
        return 2
    if p1[0] > SCREEN_HALF_SIZE[0]/2:
        return 3
    if p1[1] > SCREEN_HALF_SIZE[1]/2:
        return 4
    return 0

def karthus_ult(LIST, r, TRAILS):
    # print(r)
    for b in LIST:
        np = mult(b.pos, (r))
        b.pos = np
        # b.pos = add(b.pos, np)
        b.velocity = mult(b.velocity, r)
    for i in range(len(TRAILS)):
        for j in range(len(TRAILS[i])):
            np = mult(TRAILS[i][j], r)
            TRAILS[i][j] = np
            # TRAILS[i][j] = add(TRAILS[i][j], np)

def keep_in_line(LIST, tr):
    for b in LIST:
        p = (is_sus(b.pos))
        if p != 0:
            if p == 1: # left 
                d = b.pos[0] + 0.5*SCREEN_HALF_SIZE[0]
                r = (0.5*SCREEN_HALF_SIZE[0])/(0.5*SCREEN_HALF_SIZE[0]+d)
            if p == 2: # top
                d = b.pos[1] + 0.5*SCREEN_HALF_SIZE[1]
                r = (0.5*SCREEN_HALF_SIZE[1])/(0.5*SCREEN_HALF_SIZE[1]+d)
            if p == 3: # right 
                d = b.pos[0] - 0.5*SCREEN_HALF_SIZE[0]
                r = (0.5*SCREEN_HALF_SIZE[0])/(0.5*SCREEN_HALF_SIZE[0]+d)
            if p == 4: # bottom
                d = b.pos[1] - 0.5*SCREEN_HALF_SIZE[1] 
                r = (0.5*SCREEN_HALF_SIZE[1])/(0.5*SCREEN_HALF_SIZE[1]+d)
            # print('r is', r)
            karthus_ult(LIST, r, tr)

def center_the_shit(LIST, TRAILS):
    c = (0,0)
    for b in LIST:
        c = (c[0] + b.pos[0], c[1] + b.pos[1])
    c = (c[0]/len(LIST), c[1]/len(LIST))
    
    for b in LIST:
        b.pos = sub(b.pos, c)

    for i in range(len(TRAILS)):
        for j in range(len(TRAILS[i])):
            # np = mult(TRAILS[i][j], r)
            TRAILS[i][j] = sub(TRAILS[i][j], c)
