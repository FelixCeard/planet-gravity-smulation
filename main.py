import pygame
import sys
from functions import *
import time 
import os
from os.path import isfile, join
colors = [
    '#2a9d8f',
    '#e9c46a',
    '#f4a261',
    '#e76f51'
    '#ffafcc' # scheme 2
    '#cdb4db',
    '#ffc8dd',
    '#bde0fe',
    '#a2d2ff',
    '#f1faee'
]

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

myfont = pygame.font.SysFont('Corbel', 62)
textsurface = myfont.render('Space stuff and so', True, colors[7])
point = sub(add( (-0.8*SCREEN_HALF_SIZE[0], -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), (0, 70))

SCREEN_SIZE = (1920, 1080)
screen = pygame.display.set_mode(SCREEN_SIZE)

colors = [hextofloats(i) for i in colors]

BODYS = []
BODYS.append(Body((0,0), 1000000, vel = (1, 2), a = 0.5, color=colors[3]))
BODYS.append(Body((100,-200), 1000000, vel = (1.8, -0.1), a = 0.5, color=colors[2]))
BODYS.append(Body((200,10), 1000000, vel = (1,1), a = 0.5, color=colors[5]))
BODYS.append(Body((-200,100), 1000000, vel = (2,0), a = 0.5, color=colors[6]))
BODYS.append(Body((250,0), 1000000, vel = (1.9,-0.5), a = 0.5, color=colors[7]))

tick_num = 0

TRAILS = [[b.pos] for b in BODYS]

b1_variable = False
b2_variable = False
b3_variable = False

MOUSE_PRESSED = (0, 0)

b1_pressed = False
just_clicked = False

while (True):
    trail_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
    trail_screen = trail_screen.convert_alpha()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEMOTION:
            MOUSE_POSITION = event.pos
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q: 
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if b1_pressed == True and just_clicked == False:
                BODYS, TRAILS = place_astre(event.pos, BODYS, TRAILS)
                just_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            MOUSE_PRESSED = event.pos
            
    
    screen.fill("#2a2a2a")

    # inner rectangle
    # pygame.draw.line(screen, '#bde0fe', add((-0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    # pygame.draw.line(screen, '#bde0fe', add((-0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((-0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    # pygame.draw.line(screen, '#bde0fe', add((-0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    # pygame.draw.line(screen, '#bde0fe', add((0.5*SCREEN_HALF_SIZE[0], 0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.5*SCREEN_HALF_SIZE[0], -0.5*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))

    pygame.draw.line(screen, '#bde0fe', add((-0.8*SCREEN_HALF_SIZE[0], -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.8*SCREEN_HALF_SIZE[0], -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    pygame.draw.line(screen, '#bde0fe', add((-0.8*SCREEN_HALF_SIZE[0], -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((-0.8*SCREEN_HALF_SIZE[0], 0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    pygame.draw.line(screen, '#bde0fe', add((-0.8*SCREEN_HALF_SIZE[0], 0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.8*SCREEN_HALF_SIZE[0], 0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))
    pygame.draw.line(screen, '#bde0fe', add((0.8*SCREEN_HALF_SIZE[0], 0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE), add((0.8*SCREEN_HALF_SIZE[0], -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE))    

    if len(BODYS) > 1:
        calc_forces(BODYS)
        has_zoomed_out = keep_in_line(BODYS, TRAILS)
        center_the_shit(BODYS, TRAILS)
        if (has_zoomed_out == False):
            auto_zoom(BODYS, TRAILS)

    screen.blit(textsurface, point)

    b1 = draw_button((0,0), "Add point")
    b1_p = add((-SCREEN_HALF_SIZE[0] + 20, -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE)

    b2 = draw_button((0,0), "clear the board")
    b2_p = add((-SCREEN_HALF_SIZE[0] + 20, -0.8*SCREEN_HALF_SIZE[1]+20 + b1.get_height()), SCREEN_HALF_SIZE)
    if hovered(b2, b2_p, MOUSE_POSITION):
        b2 = draw_button((0,0), "clear the board", background_col="#202020")
        b2_p = add((-SCREEN_HALF_SIZE[0] + 20, -0.8*SCREEN_HALF_SIZE[1]+20 + b1.get_height()), SCREEN_HALF_SIZE)
    
    b3 = draw_button((0,0), "Record")
    b3_p = add((0.8*SCREEN_HALF_SIZE[0] + 20, -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE)
    if hovered(b3, b3_p, MOUSE_POSITION):
        # b1.fill()
        b3 = draw_button((0,0), "Record", background_col="#202020")
        b3_p = add((0.8*SCREEN_HALF_SIZE[0] + 20, -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE)
    
    if clicked(b3, b3_p, MOUSE_PRESSED):
        if (b3_variable == False): # start the recording
            if (os.path.exists('./TEMP') == False):
                os.mkdir('TEMP')
            else:
                onlyfiles = [f for f in os.listdir('./TEMP') if isfile(join('/TEMP', f))]
                for f in onlyfiles:
                    os.remove('./TEMP/'+f)
            b3_variable = True
        # else:
        #     b3_variable = False
            # TODO stop the recording

    if clicked(b2, b2_p, MOUSE_PRESSED):
        BODYS = []
        TRAILS = []

    if b1_pressed == False:
        if clicked(b1, b1_p, MOUSE_PRESSED):
            # print('switched it to true')
            b1_pressed = True
        if hovered(b1, b1_p, MOUSE_POSITION):
            # b1.fill()
            b1 = draw_button((0,0), "Add point", background_col="#202020")
            b1_p = add((-SCREEN_HALF_SIZE[0] + 20, -0.8*SCREEN_HALF_SIZE[1]), SCREEN_HALF_SIZE)

    if just_clicked == True:
        # print('switched it back to false')
        just_clicked = False
        b1_pressed = False
        MOUSE_PRESSED = (0,0)
    
    screen.blit(b1, b1_p)
    screen.blit(b2, b2_p)
    screen.blit(b3, b3_p)

    if len(BODYS) > 0:
        for i in range(len(BODYS)):
                b = BODYS[i]
                b.draw()
                if (tick_num % 5) == 0: 
                    # print("added points")
                    TRAILS[i].append(b.pos)
                    MAXLEN = 400
                    if (len(TRAILS[i]) > MAXLEN):
                        TRAILS[i].pop(0)
                    halfLEN = int(MAXLEN/2)
                k = [add(t, SCREEN_HALF_SIZE) for t in TRAILS[i] if in_screen(t)]
                if len(k) >= 2:
                    pygame.draw.lines(trail_screen, alpha(b.color), False, k, 2)
    tick_num += 1
    screen.blit(trail_screen, (0, 0))

    # add the fps
    screen.blit(update_fps(clock, myfont), (10,0))

    pygame.display.update()
    # print(b3_variable, ' - ', tick_num)
    if b3_variable == True:
        if (tick_num % 60) == 0:
            record(screen, tick_num)
    clock.tick(60)
    