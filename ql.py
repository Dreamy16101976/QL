# -----------------------------------------------------------------------------
# Desperate tourist
# Copyright (C) 2019 Alexey "FoxyLab" Voronin
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
# -----------------------------------------------------------------------------
# Credits:
# Icon mades by Freepik, Skyclick, xnimrodx, surang from www.flaticon.com
import math
import random
from dataclasses import dataclass
import numpy as np
import pygame
import sys
import time

from settings import *

# position and reward calculation
def action(x, y, a):
    # new position calculation
    flag = NONE_FLAG # flag reset
    # deltas initialization
    dx = 0
    dy = 0
    if (a == 0): # N
        if (y > 0):
            dy = -1
    elif (a == 1): # NE
        if ((y > 0) and (x < (SIZE-1))):
            dy = -1
            dx = 1
    elif (a == 2): # E
        if (x < (SIZE-1)):
            dx = 1
    elif (a == 3): # SE
        if ((y < (SIZE-1)) and (x < (SIZE-1))):
            dy = 1
            dx = 1
    elif (a == 4): # S
        if (y < (SIZE-1)):
            dy = 1
    elif (a == 5): # SW
        if ((y < (SIZE-1)) and (x > 0)):
            dy = 1
            dx = -1
    elif (a == 6): # W
        if (x > 0):
            dx = -1
    elif (a == 7): # NW
        if ((y > 0) and (x >0)):
            dy = -1
            dx = -1
    if ((dx == 0) and (dy == 0)): # border
        flag = BORDER_FLAG
    if ((x+dx, y+dy) in WALLS): # wall
        dx = 0
        dy = 0
        flag = WALL_FLAG
    if ((x+dx, y+dy) in TRAPS): # trap
        dx = X_START - x
        dy = Y_START - y
        x = X_START
        y = Y_START
        flag = TRAP_FLAG
    # bonus calculation
    bonus = STEP_PENALTY # step penalty
    if (((x + dx) == X_FINISH) and ((y + dy) == Y_FINISH)): # check next position for finish
        bonus = bonus + FINISH_BONUS
        flag = FINISH_FLAG
    return dx, dy, bonus, flag

# state calculation
def state(x, y):
    return x + y*SIZE


# position
@dataclass
class Pos:
    x: int
    y: int

print("Q-learning")
np.random.seed(SEED) # PRNG initialization
episodes_max = int(input("Episodes number?")) # episode request
q = np.empty((ACTIONS, SIZE*SIZE), dtype = float) # creating an empty table Q
q[:] = np.NINF # initialization of elements of table Q
pygame.init() # Pygame initialization
pygame.display.set_caption("Q-learning")
canvas = pygame.display.set_mode((SIZE*CELL_SIZE+(SIZE-1)*BORDER_SIZE, SIZE*CELL_SIZE+(SIZE-1)*BORDER_SIZE+STATUS_SIZE))
canvas.fill(WHITE)
font = pygame.font.SysFont("comicsansms", FONT_SIZE) # font assignment
# image upload
icon = pygame.image.load("walk.png")
footprint = pygame.image.load("footprints.png")
bricks = pygame.image.load("wall.png")
sand = pygame.image.load("sand.png")
bomb = pygame.image.load("bomb.png")
start = pygame.image.load("start.png")
finish = pygame.image.load("finish.png")
walk = pygame.image.load("walk.png")
icon.convert()
pygame.display.set_icon(icon) # window icon assignment
footprint.convert()
bricks.convert()
sand.convert()
bomb.convert()
start.convert()
finish.convert()
walk.convert()
# drawing cell borders
i = 1
while (i < SIZE):
    pygame.draw.line(canvas, BLACK, (i * CELL_SIZE + (i-1) * BORDER_SIZE + 1, 0), (i * CELL_SIZE + (i-1) * BORDER_SIZE + 1, SIZE*CELL_SIZE+(SIZE-1)*BORDER_SIZE - 1), BORDER_SIZE)
    i += 1
i = 1
while (i < SIZE):
    pygame.draw.line(canvas, BLACK, (0, i * CELL_SIZE + (i-1) * BORDER_SIZE + 1), (SIZE*CELL_SIZE+(SIZE-1)*BORDER_SIZE - 1, i * CELL_SIZE + (i-1) * BORDER_SIZE + 1), BORDER_SIZE)
    i += 1
episode = 0 # episode counter reset
while (episode < episodes_max): # episode cycle
    print("EPISODE: " + str(episode + 1)) # episode number output
    # epsilon calculation
    if (episode == (episodes_max - 1)):
        # testing (last episode)
        epsilon = 0.0
    else:
        # training
        epsilon = ((episodes_max-1) - episode)/(episodes_max - 1) *(EPSILON_START-EPSILON_FINISH) + EPSILON_FINISH
    print("EPSILON: ", format(epsilon, '.2f')) # вывод значения эпсилон
    # cell fill
    i = 0
    while (i < SIZE):
        j = 0
        while (j < SIZE):
            canvas.blit(sand, (j*(CELL_SIZE+BORDER_SIZE) , i*(CELL_SIZE+BORDER_SIZE)))
            j += 1
        i += 1
    # drawing walls
    for wall in WALLS:
        canvas.blit(bricks, (wall[0]*(CELL_SIZE+BORDER_SIZE) , wall[1]*(CELL_SIZE+BORDER_SIZE)))
    # drawing traps
    for trap in TRAPS:
        canvas.blit(bomb, (trap[0]*(CELL_SIZE+BORDER_SIZE) , trap[1]*(CELL_SIZE+BORDER_SIZE)))
    moving = True # moving flag up
    pos = Pos(X_START, Y_START) # agent position initialization
    canvas.blit(walk, (pos.x*(CELL_SIZE+BORDER_SIZE) , pos.y*(CELL_SIZE+BORDER_SIZE))) # drawing agent
    f = NONE_FLAG
    step = 0 # step counter reset
    scores = 0.0 # reward counter reset
    canvas.blit(finish, (X_FINISH*(CELL_SIZE+BORDER_SIZE) , Y_FINISH*(CELL_SIZE+BORDER_SIZE))) # drawing end position
    while (moving):
        pygame.event.pump()
        # drawing
        canvas.blit(sand, (pos.x*(CELL_SIZE+BORDER_SIZE) , pos.y*(CELL_SIZE+BORDER_SIZE)))
        canvas.blit(walk, (pos.x*(CELL_SIZE+BORDER_SIZE) , pos.y*(CELL_SIZE+BORDER_SIZE)))
        canvas.fill(WHITE, pygame.Rect(0, SIZE*CELL_SIZE+SIZE*BORDER_SIZE, SIZE*CELL_SIZE+(SIZE-1)*BORDER_SIZE, STATUS_SIZE))
        text = font.render("E:"+str(episode + 1),True,(BLUE))
        canvas.blit(text,(1, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        text = font.render("S:"+str(step),True,(BLUE))
        canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        text = font.render("X:"+str(pos.x)+" Y:"+str(pos.y),True,(BLUE))
        canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) * 2 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        text = font.render(format(scores, '.2f'),True,(RED))
        canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) * 3 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        if ((episode == (episodes_max-1)) and ((f == BORDER_FLAG) or (f == WALL_FLAG))):
            text = font.render("LOCK",True,(RED))
            canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) *4 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
            pygame.display.flip() # display update
            print("LOCK") # total scores
            break
        if (f == FINISH_FLAG): # episode is over            
            # optimal actions display
            i = 0
            while (i < SIZE*SIZE):
                zero = True
                # search for the first explored action
                j = 0
                while (j < ACTIONS):
                    if (np.isneginf(q[j, i]) ==  False):
                        zero = False # explored action found
                        break
                    j += 1 # next action
                if (zero == False): # explored action exist
                    max = q[j, i] # current max q-value
                    k = j # current optimal action
                    j += 1 # next action
                    while (j < ACTIONS):
                        # check for not nan
                        if (np.isneginf(q[j, i]) ==  False):
                            # check for max
                            if (q[j, i] > max):
                                max = q[j, i] # new max q-value
                                k = j # new optimal action
                        j += 1 # next action
                    print(DIRS[k], end = '')
                else:
                    print("-", end = '')
                i += 1
                if ((i % SIZE) == 0):
                    print("")
            text = font.render("FINISH",True,(BLUE))
            canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) *4 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
            pygame.display.flip() # display update
            print("SCORES = " + format(scores, '.2f')) # total scores
            time.sleep(EPISODE_PAUSE)
            break
        if (f == WALL_FLAG):
            text = font.render("WALL",True,(RED))
            canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) *4 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        elif (f == TRAP_FLAG):
            text = font.render("TRAP",True,(RED))
            canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) *4 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        elif (f == BORDER_FLAG):
            text = font.render("BORDER",True,(RED))
            canvas.blit(text,((SIZE*CELL_SIZE+SIZE*BORDER_SIZE) *4 // 5, SIZE*CELL_SIZE+SIZE*BORDER_SIZE+5))
        pygame.display.flip() # display update
        pygame.event.pump()
        # задержка шага
        if (episode == (episodes_max-1)):
            time.sleep(STEP_PAUSE) # testing pause
        else:
            time.sleep(LRN_PAUSE) # learning pause
        # random strategy selection
        if (np.random.rand() < epsilon):
            # explore
            a = np.random.randint(0, ACTIONS)
        else:
            # exploit
            zero = True
            # find first not nan
            j = 0
            while (j < ACTIONS):
                if (np.isneginf(q[j, state(pos.x, pos.y)]) ==  False):
                    zero = False # explored action found
                    break
                j += 1 # next action
            if (zero == False): # explored action exist
                max = q[j, state(pos.x, pos.y)] # current max q-value
                k = j # current optimal action
                j += 1 # next action
                while (j < ACTIONS):
                    # check for not nan
                    if (np.isneginf(q[j, state(pos.x, pos.y)]) ==  False):
                        # check for max
                        if (q[j, state(pos.x, pos.y)] > max):
                            max = q[j, state(pos.x, pos.y)] # new max q-value
                            k = j # new optimal action
                    j += 1 # next action
                # exploit
                a = k # optimal action select
            else: # no action explored
                # explore
                a = np.random.randint(0, ACTIONS) # random action select
        # 
        dx, dy, r, f = action(pos.x, pos.y, a)
        if ((dx != 0) or (dy != 0)): # agent moves
            canvas.blit(sand, (pos.x*(CELL_SIZE+BORDER_SIZE) , pos.y*(CELL_SIZE+BORDER_SIZE))) # clean source cell
            canvas.blit(footprint, (pos.x*(CELL_SIZE+BORDER_SIZE) , pos.y*(CELL_SIZE+BORDER_SIZE))) # footprint drawing
        # q-table update
        if (episode != (episodes_max-1)):
            if (np.isneginf(q[a, state(pos.x, pos.y)]) ==  False):
                if (np.isneginf(np.max(q[:, state(pos.x+dx, pos.y+dy)])) == False):
                    q[a, state(pos.x, pos.y)] = q[a, state(pos.x, pos.y)] + ALPHA*(r + GAMMA*np.max(q[:, state(pos.x+dx, pos.y+dy)]) - q[a, state(pos.x, pos.y)])
                else:
                    q[a, state(pos.x, pos.y)] = q[a, state(pos.x, pos.y)] + ALPHA*(r - q[a, state(pos.x, pos.y)])
            else:
                if (np.isneginf(np.max(q[:, state(pos.x+dx, pos.y+dy)])) == False):
                    q[a, state(pos.x, pos.y)] = ALPHA*(r + GAMMA*np.max(q[:, state(pos.x+dx, pos.y+dy)]))
                else:
                    q[a, state(pos.x, pos.y)] = ALPHA*r
        scores = scores + r # scores update
        # moving an agent to a new cell
        pos.x = pos.x + dx
        pos.y = pos.y + dy
        step += 1 # increment step counter
        pygame.event.pump()
        for event in pygame.event.get(): # event checking
            if event.type == pygame.QUIT:
                sys.exit(0) # exit from the program
    episode += 1 # increment episode counter
while (True): # waiting for window to close
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0) # exit from the program
