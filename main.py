import random

import pygame
import math

import objects
from draw import *

# pygame initialization stuff, based on documentation
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fps = 60

# variables for the box
boxes = []

for i in range(8):
    for j in range(8):
        boxes.append(objects.Body(i * 100, j * 100))
        boxes[i * 8 + j].mass = math.sqrt(random.randint(1, 150))
"""
boxes.append(objects.Body(100, 300))
boxes.append(objects.Body(400, 300))
boxes[0].Vx = 5
boxes[0].mass = 4
boxes[1].Vx = 2
boxes[1].mass = 5"""



# for orbits
attractor = [640, 360, 32]
orbiting = False
dist = 64
phi = 0

# so that it can be paused
running = False
spaceIsPressed = False

# stuff for selecting vectors
selected = -1
selectToggle = True

# toggle for pushing buttons
buttonToggle = True


looping = True
while looping:
    # get position of mouse
    mouse = pygame.mouse.get_pos()

    # if you press the close button, quit the while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False

    # clear screen for a new frame
    screen.fill((255, 255, 255))

    # pause the game if you press space
    if pygame.key.get_pressed()[pygame.K_SPACE] and not spaceIsPressed:
        selected = -1
        running = not running

        spaceIsPressed = True
    spaceIsPressed = pygame.key.get_pressed()[pygame.K_SPACE]

    if running:
        for i in boxes:
            i.step()

    # drawing stuffs
    for i in range(len(boxes)):
        boxes[i].draw(screen)
        draw_vector(screen, boxes[i].Vx, boxes[i].Vy, boxes[i].x, boxes[i].y)  # velocity arrow

    for i in boxes:
        for j in range(len(i.Fx)):
            i.draw_force(screen, i)
    """
    if orbiting:
        draw_vector(screen, attractor[2] * mass / dist * math.cos(phi), attractor[2] * mass / dist * math.sin(phi), x, y,
                    (0, 100, 0))
        pygame.draw.circle(screen, (0, 0, 0), (attractor[0], attractor[1]), 5)"""

    # interactions with other boxes
    if running:
        for i in range(len(boxes)):
            for j in range(len(boxes)):
                if i != j:
                    boxes[i].calc_gravity(screen, boxes[j].x, boxes[j].y, boxes[j].mass)
                    boxes[i].calc_collision(screen, boxes[j])


    # UI and buttons
    """
    if not running:
        display_ui(screen)
        if pygame.mouse.get_pressed(3)[0] and screen.get_width() * 0.775 < mouse[0] < screen.get_width() * 0.975 and buttonToggle:
            # add new force
            if screen.get_height() * 0.05 < mouse[1] < screen.get_height() * 0.2:
                buttonToggle = False
                Fx.append(0)
                Fy.append(0)
                selected = len(Fx) - 1
            if screen.get_height() * 0.25 < mouse[1] < screen.get_height() * 0.4:
                buttonToggle = False
                Fx.pop(selected)
                Fy.pop(selected)
                selected = -1
            if screen.get_height() * 0.45 < mouse[1] < screen.get_height() * 0.6:
                buttonToggle = False
                orbiting = not orbiting
            if screen.get_height() * 0.65 < mouse[1] < screen.get_height() * 0.8:
                buttonToggle = False
            if screen.get_height() * 0.85 < mouse[1] < screen.get_height():
                buttonToggle = False
                x, y = screen.get_width() * 0.375, screen.get_height() * 0.5
                theta = .8
                Vx, Vy = 0, 0
                Fx = [0]
                Fy = [-19.6]
                orbiting = False

        buttonToggle = not pygame.mouse.get_pressed(3)[0]
        """

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
