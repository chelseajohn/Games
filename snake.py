# -*- coding: utf-8 -*-
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox


class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx,
                    self.pos[1] + self.dirny)  # change position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # Width/Height of each cube
        i = self.pos[0]  # current row
        j = self.pos[1]  # current column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))

        if eyes:    # draw eyes
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis - radius*2, j*dis+8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)   # head is the front of the snake
        self.body.append(self.head)  # adding the head to snake body
        # snake directions
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # checks if the usewr hit the red X
                pygame.quit()

            keys = pygame.key.get_pressed()  # gets the user pressed keys

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):  # loop through every cube in snake body
            p = c.pos[:]    # cube posiiton on grid
            if p in self.turns:  # cube curent posiiton is where we turned
                turn = self.turns[p]  # get direction to turn
                c.move(turn[0], turn[1])  # move cube in that direction
                if i == len(self.body)-1:  # if last cube then remove from dict
                    self.turns.pop(p)
            else:  # if we are not truning the cube
                if c.dirnx == -1 and c.pos[0] <= 0:
                    # if edge of window then appear on opposite side
                    c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows-1)
                else:
                    # move in current direction if not at edge
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)  # eyes for head
            else:
                c.draw(surface)  # just cube for body


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows  # spacing btw lines

    x = 0  # current x
    y = 0   # current y
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (0, 0, 0), (x, 0), (x, w))
        pygame.draw.line(surface, (0, 0, 0), (0, y), (w, y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((255, 255, 255))  # game screen background fill
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)  # draws grid lines
    pygame.display.update()  # update screen


def randomSnack(rows, item):

    positions = item.body  # positions of cubes of snake

    while True:  # Keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
             # This wll check if the position we generated is occupied by the snake
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global width, rows, s, snack
    width = 500  # width of the game window screen
    rows = 20     # rows of the game window

    win = pygame.display.set_mode((width, width))  # creates the game window
    s = snake((255, 0, 0), (10, 10))   # creates the snake object
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()  # creating a clock object

    while flag:  # Main loop
        pygame.time.delay(50)  # delay to not run quickly
        clock.tick(8)  # fps
        s.move()

        if s.body[0].pos == snack.pos:  # Checks if the head collides with the snack
            s.addCube()  # adds cube to snake
            snack = cube(randomSnack(rows, s), color=(
                0, 255, 0))  # creates snack object

        for x in range(len(s.body)):
            # checking overlap
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                break

        redrawWindow(win)  # refresh the game window


main()
