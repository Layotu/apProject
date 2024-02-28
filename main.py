import pygame
import math

# pygame initialization stuff, based on docs
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fps = 30

# kinematics stuffs
x, y = screen.get_width() / 2, screen.get_height() / 2
Vx, Vy = 15, 15

# arrays for list of forces
Fx = [0]
Fy = [-9.8]

# so that it can be paused
running = False
spaceIsPressed = False


def drawVector(horizontal, vertical, color=(0, 0, 0)):
    pygame.draw.aaline(screen, color, (x, y), (x + horizontal * 8, y - vertical * 8))
    theta = math.atan2(vertical, horizontal)
    pygame.draw.aaline(screen, color, (x + horizontal * 8, y - vertical * 8), (x + horizontal * 8 - max(math.sqrt(horizontal**2 + vertical**2), 8) * math.cos(theta + 0.5), y - vertical * 8 + max(math.sqrt(horizontal**2 + vertical**2), 8) * math.sin(theta + 0.5)))
    pygame.draw.aaline(screen, color, (x + horizontal * 8, y - vertical * 8), (x + horizontal * 8 - max(math.sqrt(horizontal**2 + vertical**2), 8) * math.cos(theta - 0.5), y - vertical * 8 + max(math.sqrt(horizontal**2 + vertical**2), 8) * math.sin(theta - 0.5)))


looping = True
while looping:
    # if you press the close button or the escape button, quit the while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False

    # pause the game if you press space
    if pygame.key.get_pressed()[pygame.K_SPACE] and not spaceIsPressed:
        running = not running
        spaceIsPressed = True
    elif not pygame.key.get_pressed()[pygame.K_SPACE]:
        spaceIsPressed = False

    # kinematics stuff to update values
    if running:
        for i in Fx:
            Vx += i / 4
        for i in Fy:
            Vy += i / 4

        x += Vx
        y -= Vy


    # drawing stuffs
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(x - 25, y - 25, 50, 50))
    drawVector(Vx / 2, Vy / 2)
    for i in range(len(Fx)):
        drawVector(Fx[i], Fy[i], (100, 0, 0))




    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
