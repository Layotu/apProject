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
newBox = True
newCoords = []

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
newForce = False
newForceCoords = []

# toggle for pushing buttons
buttonToggle = True

# settings stuff
font = pygame.font.SysFont("Jetbrains Mono", 25)
blockAttraction = False
friction = False
collision = True
gravity = True

print("controls:")
print("rt click and drag: add new box")
print("1: toggle friction")
print("2: toggle gravity")
print("3: toggle collision")

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

    # toggle things if you press buttons
    # pause / play when space is pressed
    if pygame.key.get_pressed()[pygame.K_SPACE] and not spaceIsPressed:
        running = not running
        spaceIsPressed = True
    spaceIsPressed = pygame.key.get_pressed()[pygame.K_SPACE]
    # friction toggled with 1 key
    if pygame.key.get_pressed()[pygame.K_1] and buttonToggle:
        friction = not friction
        buttonToggle = False
    # attraction toggled with 2 key
    if pygame.key.get_pressed()[pygame.K_2] and buttonToggle:
        blockAttraction = not blockAttraction
        buttonToggle = False
    # collision toggled with 3 key
    elif pygame.key.get_pressed()[pygame.K_3] and buttonToggle:
        collision = not collision
        buttonToggle = False
    # gravity toggled with 4 key
    elif pygame.key.get_pressed()[pygame.K_4] and buttonToggle:
        gravity = not gravity
        buttonToggle = False
    # reset button detection
    elif not pygame.key.get_pressed()[pygame.K_4] and not pygame.key.get_pressed()[pygame.K_3] and not pygame.key.get_pressed()[pygame.K_2] and not pygame.key.get_pressed()[pygame.K_1] and not buttonToggle:
        buttonToggle = True

    # add new boxes
    if pygame.mouse.get_pressed(3)[2] and newBox:
        newCoords = [mouse[0], mouse[1]]
        newBox = False
    elif not pygame.mouse.get_pressed(3)[2] and not newBox:
        width = math.sqrt((newCoords[0] - mouse[0]) ** 2 + (newCoords[1] - mouse[1]) ** 2)
        boxes.append(objects.Body(newCoords[0], newCoords[1]))
        boxes[len(boxes) - 1].mass = max(width / 32, 1)
        newBox = True
    elif not newBox:
        width = math.sqrt((newCoords[0] - mouse[0]) ** 2 + (newCoords[1] - mouse[1]) ** 2)
        text = font.render("Mass: " + str(round(max(width / 32, 1) * 100) / 100.0), True, 0)
        width = (width / 32) ** 0.3333 * 6
        screen.blit(text, (newCoords[0] - width, newCoords[1] - width - 20))
        pygame.draw.rect(screen, (200, 255, 200), rect=(newCoords[0] - width, newCoords[1] - width, width * 2, width * 2))

    # add forces to boxes
    if pygame.mouse.get_pressed(3)[0] and not newForce:
        newForceCoords = [mouse[0], mouse[1]]
        newForce = True

    # update boxes
    if gravity and running:
        for i in boxes:
            i.step(friction)
            i.wall_collision(screen)
    elif running:
        for i in boxes:
            i.step(friction)
            i.wall_collision(screen)

    # interactions with other boxes
    if running:
        for i in range(len(boxes)):
            for j in range(len(boxes)):
                if i != j:
                    if blockAttraction:
                        boxes[i].calc_gravity(screen, boxes[j].x, boxes[j].y, boxes[j].mass)
                    if collision:
                        boxes[i].calc_collision(screen, boxes[j])

    # drawing stuffs
    for i in range(len(boxes)):
        boxes[i].draw(screen)
        draw_vector(screen, boxes[i].Vx, boxes[i].Vy, boxes[i].x, boxes[i].y)  # velocity arrow
        for j in range(len(boxes[i].forces) - 1):
            boxes[i].draw_force(screen, i)

    """
    if orbiting:
        draw_vector(screen, attractor[2] * mass / dist * math.cos(phi), attractor[2] * mass / dist * math.sin(phi), x, y,
                    (0, 100, 0))
        pygame.draw.circle(screen, (0, 0, 0), (attractor[0], attractor[1]), 5)"""

    # setting display
    if running:
        text = font.render("Playing", True, 0)
        screen.blit(text, (5, 5))
    else:
        text = font.render("Paused", True, 0)
        screen.blit(text, (5, 5))
    if friction:
        text = font.render("Friction On", True, 0)
        screen.blit(text, (5, 25))
    else:
        text = font.render("Frictionless", True, 0)
        screen.blit(text, (5, 25))
    if blockAttraction:
        text = font.render("Gravity between blocks On", True, 0)
        screen.blit(text, (5, 45))
    else:
        text = font.render("No gravity between blocks", True, 0)
        screen.blit(text, (5, 45))
    if collision:
        text = font.render("Collision On", True, 0)
        screen.blit(text, (5, 65))
    else:
        text = font.render("No collision", True, 0)
        screen.blit(text, (5, 65))
    if gravity:
        text = font.render("Gravity On", True, 0)
        screen.blit(text, (5, 85))
    else:
        text = font.render("No Gravity", True, 0)
        screen.blit(text, (5, 85))

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
