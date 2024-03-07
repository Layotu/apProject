import pygame
from pygame.math import *
import math

from draw import *

# pygame initialization stuff, based on docs
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Jetbrains Mono", 15)

fps = 60

# variables for the box
x = round(screen.get_width() * 0.375)
y = round(screen.get_height() * 0.5)
theta = math.pi/4
mass = 8
Vx, Vy = 0, 0
Wx, Wy = 0, 0
mu = 0.1
history = []

# forces stuff
forces = [Vector2(0, -4.9)]
sizeMult = 8

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

# self explanitory
wallCollision = True


# returns a vector2 of the normal force
def calc_normal():
    output = Vector2()
    if x <= 20 or x >= screen.get_width() * 0.75 - 20:
        output.x = -1
    if y <= 20 or y >= screen.get_height() - 20:
        output.y = -1
    output.x *= calc_net_force().x
    output.y *= calc_net_force().y
    return output


# returns a vector2 of the net force
def calc_net_force():
    net = Vector2()
    for i in forces:
        net.x += i.x
        net.y += i.y
    return net


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
        # kinematics stuff to update values
        for i in forces:
            Vx += i.x / mass
            Vy += i.y / mass

        if wallCollision:
            Vx += calc_normal().x / mass
            Vy += calc_normal().y / mass

            if abs(Vx) > 0:
                Vx -= (max(abs(Vx), 0) / Vx) * calc_normal()[1] * mu
            if abs(Vy) > 0:
                Vy -= (max(abs(Vy), 0) / Vy) * calc_normal()[0] * mu

            x = min(max(40, x), int(screen.get_width() * 0.75 - 40))
            y = min(max(40, y), int(screen.get_height() - 40))

        x += Vx
        y -= Vy

        history.insert(0, [x, y])
        history = history[0:60]

    # code for orbit mode
    if orbiting:
        # fun trig stuff to calculate change in horizontal and vertical velocities
        dist = math.sqrt((attractor[0] - x) ** 2 + (attractor[1] - y) ** 2)
        phi = math.atan2(-(attractor[1] - y), (attractor[0] - x))
        if running:
            Vx += attractor[2] * mass / dist * math.cos(phi) / 2
            Vy += attractor[2] * mass / dist * math.sin(phi) / 2

    # selecting and moving vectors
    if pygame.mouse.get_pressed(3)[0] and selectToggle:
        for i in range(len(forces)):
            if abs(x + forces[i].x * sizeMult - mouse[0]) < 32 and abs(y - forces[i].y * sizeMult - mouse[1]) < 32:
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
            forces[selected].x = (mouse[0] - x) / sizeMult
            forces[selected].y = -(mouse[1] - y) / sizeMult
    selectToggle = not pygame.mouse.get_pressed(3)[0]

    # information stuff
    coords = font.render(
        "X: " + str(round(x * 100) / 100.0) + " Y: " + str(round(y * 100) / 100.0) + " θ: " + str(round(
            theta - math.pi/4) / 100.0), True, 0)
    kinematics = font.render(
        "Speed: " + str(round(math.sqrt(Vx ** 2 + Vy ** 2) * 100) / 100.0) + " Mass: " + str(
            round(mass * 100) / 100.0), True, 0)
    k = round(0.5 * mass * (Vx ** 2 + Vy ** 2)) / 10.0
    ug = round(mass * .1 * (screen.get_height() - y - 32)) / 10.0

    energy = font.render("Fn: " + str(round(math.sqrt(max(calc_normal()[0], 0) ** 2 + max(calc_normal()[1], 0) ** 2) * 100) / 100.0)
                     + " Ff: " + str(round(math.sqrt(calc_normal()[0] ** 2 + calc_normal()[1] ** 2) * mu * 100) / 100.0), True, 0)
    screen.blit(coords, (x - 32, y - 32 - 20))
    screen.blit(kinematics, (x - 32, y - 32 - 10))
    screen.blit(energy, (x - 32, y - 32))

    # drawing stuffs
    for i in range(len(history)):
        pygame.draw.circle(screen, (i * 4, i * 4, i * 4), (history[i][0], history[i][1]), 2)    # trail
    draw_player(screen, x, y, theta)
    draw_vector(screen, Vx / 4 * sizeMult, Vy / 4 * sizeMult, x, y)
    if wallCollision and calc_normal().magnitude() > 0:
        draw_vector(screen, calc_normal()[0] * sizeMult, calc_normal()[1] * sizeMult, x, y, (0, 0, 100))
    for i in forces:
        draw_vector(screen, i.x * sizeMult, i.y * sizeMult, x, y, (100, 0, 0))
    if orbiting:
        draw_vector(screen, attractor[2] * mass / dist * math.cos(phi), attractor[2] * mass / dist * math.sin(phi), x, y,
                    (0, 100, 0))
        pygame.draw.circle(screen, (0, 0, 0), (attractor[0], attractor[1]), 5)

    # UI and buttons
    display_ui(screen)
    if pygame.mouse.get_pressed(3)[0] and screen.get_width() * 0.775 < mouse[0] < screen.get_width() * 0.975 and buttonToggle:
        # add new force
        if screen.get_height() * 0.05 < mouse[1] < screen.get_height() * 0.2:
            buttonToggle = False
            running = False
            forces.append(Vector2())
            selected = len(forces) - 1
        if screen.get_height() * 0.25 < mouse[1] < screen.get_height() * 0.4:
            buttonToggle = False
            forces.pop(selected)
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
            forces = [Vector2(0, -.98)]
            orbiting = False

    buttonToggle = not pygame.mouse.get_pressed(3)[0]

    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
