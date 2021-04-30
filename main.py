import pygame
import sys
from functions import *

pygame.init()

SCREEN_SIZE = (1920, 1080)
screen = pygame.display.set_mode(SCREEN_SIZE)



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
    10000, 
    1, 
    5,
    # (-20, 0),
    (random.randrange(-1, 1)*random.random(),random.randrange(-1, 1)*random.random()),
    random.choice(colors)) for i in range(10)]

# BODYS = []
# BODYS.append(Body((0,0), 50000, vel = (1, -2), a = 0.3, color=colors[3]))
# BODYS.append(Body((100,-200), 50000, vel = (2.8, -0.1), a = 0.3, color=colors[2]))
# BODYS.append(Body((200,10), 50000, vel = (0,0), color=colors[5]))

tick_num = 0

# center = get_center(BODYS)
# center_diff = (SCREEN_SIZE[0]/2 - center[0], SCREEN_SIZE[1]/2 - center[1])
# for b in BODYS:
#     b.pos = (b.pos[0] + center_diff[0], b.pos[1] + center_diff[1])
TRAILS = [[b.pos] for b in BODYS]

while (True):
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q: 
                sys.exit()
            if event.key == pygame.K_s:
                center_da_bodys(BODYS)
    
    screen.fill("#2a2a2a")
    
    pygame.draw.line(screen, '#bde0fe', (0.25*SCREEN_SIZE[0], 0.25*SCREEN_SIZE[1]), (0.75*SCREEN_SIZE[0], 0.25*SCREEN_SIZE[1]))
    pygame.draw.line(screen, '#bde0fe', (0.25*SCREEN_SIZE[0], 0.25*SCREEN_SIZE[1]), (0.25*SCREEN_SIZE[0], 0.75*SCREEN_SIZE[1]))
    pygame.draw.line(screen, '#bde0fe', (0.25*SCREEN_SIZE[0], 0.75*SCREEN_SIZE[1]), (0.75*SCREEN_SIZE[0], 0.75*SCREEN_SIZE[1]))
    pygame.draw.line(screen, '#bde0fe', (0.75*SCREEN_SIZE[0], 0.75*SCREEN_SIZE[1]), (0.75*SCREEN_SIZE[0], 0.25*SCREEN_SIZE[1]))

    # draw the center
    # pygame.draw.circle(screen, '#bde0fe', (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2), radius=2)


    keep_in_line(BODYS, TRAILS)
    center_the_shit(BODYS, TRAILS)
    calc_forces(BODYS)

    
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
                pygame.draw.lines(screen, b.color, False, k, 2)
    tick_num += 1
    pygame.display.update()