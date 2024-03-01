import pygame
import math

import objects
from draw import *

# pygame initialization stuff, based on docs
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fps = 30

# variables for the box
box = objects.Body(screen.get_width() * 0.375, screen.get_height() * 0.5)
box.add_force((0, 0), (0, -4.9))

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

    # if you press the close button or the escape button, quit the while loop
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
        box.step()

    # code for orbit mode
    """
    if orbiting:
        # fun trig stuff to calculate change in horizontal and vertical velocities
        dist = math.sqrt((attractor[0] - x) ** 2 + (attractor[1] - y) ** 2)
        phi = math.atan2(-(attractor[1] - y), (attractor[0] - x))
        if running:
            Vx += attractor[2] * mass / dist * math.cos(phi)
            Vy += attractor[2] * mass / dist * math.sin(phi)
    """

    # selecting and moving vectors
    """if pygame.mouse.get_pressed(3)[0] and selectToggle:
        for i in range(len(Fx)):
            if abs(x + Fx[i] * 8 - mouse[0]) < 20 and abs(y - Fy[i] * 8 - mouse[1]) < 20:
                if selected == i:
                    selected = -1
                else:
                    selected = i
                selectToggle = False
        if abs(attractor[0] - mouse[0]) < 20 and abs(attractor[1] - mouse[1]) < 20:
            if selected == -2:
                selected = -1
            else:
                selected = -2
    elif selected != -1:
        if selected == -2:
            attractor[0], attractor[1] = mouse
        else:
            Fx[selected] = (mouse[0] - x) / 8
            Fy[selected] = -(mouse[1] - y) / 8
    selectToggle = not pygame.mouse.get_pressed(3)[0]"""

    # drawing stuffs
    box.draw(screen)
    for i in range(len(box.Fx)):
        box.draw_force(screen, i)
    """
    if orbiting:
        draw_vector(screen, attractor[2] * mass / dist * math.cos(phi), attractor[2] * mass / dist * math.sin(phi), x, y,
                    (0, 100, 0))
        pygame.draw.circle(screen, (0, 0, 0), (attractor[0], attractor[1]), 5)"""

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
