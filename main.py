import pygame
import sys
from functions import *
import time 

pygame.init()

SCREEN_SIZE = (1920, 1080)
screen = pygame.display.set_mode(SCREEN_SIZE)

trail_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)



colors = [
    '#2a9d8f',
    '#e9c46a',
    '#f4a261',
    '#e76f51'
    '#ffafcc' # scheme 2
    '#cdb4db',
    '#ffc8dd',
    '#bde0fe',
    '#a2d2ff'
]

colors = [hextofloats(i) for i in colors]

BODYS = [Body(
    (random.randrange(-0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[0]),
    random.randrange(-0.5*SCREEN_HALF_SIZE[1], 0.5*SCREEN_HALF_SIZE[1])),
    100000, 
    1, 
    5,
    # (-20, 0),
    (random.randrange(-1, 1)*random.random(),random.randrange(-1, 1)*random.random()),
    random.choice(colors)) for i in range(50)]

BODYS = []
BODYS.append(Body((0,0), 10000, vel = (1, -2), a = 0.5, color=colors[3]))
BODYS.append(Body((100,-200), 100000, vel = (1.8, -0.1), a = 0.5, color=colors[2]))
BODYS.append(Body((200,10), 100000, vel = (-1,0), color=colors[5]))

tick_num = 0

TRAILS = [[b.pos] for b in BODYS]

while (True):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q: 
                sys.exit()
            if event.key == pygame.K_s:
                center_da_bodys(BODYS)
            if event.key == pygame.K_a:
                time.sleep(9999)
    
    screen.fill("#2a2a2a")
    trail_screen.fill('#2a2a2a')
    trail_screen.set_alpha(0.5)

    # pygame.draw.line(screen, '#bde0fe', add((-0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    # pygame.draw.line(screen, '#bde0fe', add((-0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((-0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    # pygame.draw.line(screen, '#bde0fe', add((-0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    # pygame.draw.line(screen, '#bde0fe', add((0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))

    pygame.draw.line(screen, '#bde0fe', add((-0.75*SCREEN_HALF_SIZE[0], -0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.75*SCREEN_HALF_SIZE[0], -0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    pygame.draw.line(screen, '#bde0fe', add((-0.75*SCREEN_HALF_SIZE[0], -0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((-0.75*SCREEN_HALF_SIZE[0], 0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    pygame.draw.line(screen, '#bde0fe', add((-0.75*SCREEN_HALF_SIZE[0], 0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.75*SCREEN_HALF_SIZE[0], 0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    pygame.draw.line(screen, '#bde0fe', add((0.75*SCREEN_HALF_SIZE[0], 0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.75*SCREEN_HALF_SIZE[0], -0.75*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))    

    calc_forces(BODYS)
    has_zoomed_out = keep_in_line(BODYS, TRAILS)
    center_the_shit(BODYS, TRAILS)
    if (has_zoomed_out == False):
        auto_zoom(BODYS, TRAILS)

    
    for i in range(len(BODYS)):
            b = BODYS[i]
            b.draw()
            if (tick_num % 10) == 0: 
                # print("added points")
                TRAILS[i].append(b.pos)
                MAXLEN = 5000
                if (len(TRAILS[i]) > MAXLEN):
                    TRAILS[i].pop(0)
                halfLEN = int(MAXLEN/2)
            k = [add(t, SCREEN_HALF_SIZE) for t in TRAILS[i]]
            if len(TRAILS[i]) > halfLEN:
                pygame.draw.lines(screen, alpha(b.color), False, k[:halfLEN], 2)
                pygame.draw.lines(screen, b.color, False, k[(halfLEN-1):], 2) 
            else:
                pygame.draw.lines(screen, alpha(b.color), False, k, 2)
    tick_num += 1
    # screen.blit(trail_screen, pygame.Rect(0,0,1920, 1080))
    pygame.display.update()