import pygame

# pygame initialization stuff, based on docs
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

fps = 30

# kinematics stuffs
x, y = screen.get_width() / 2, screen.get_height() / 2
Vx, Vy = 15, -15

# arrays for list of forces
Fx = [0]
Fy = [9.8]

# so that it can be paused
running = False
spaceIsPressed = False


def drawForce(horizontal, vertical):
    pygame.draw.line(screen, (0, 0, 0), (x, y), (x + horizontal, x + vertical))
    # pygame.draw.line(horizontal, vertical, horizontal + (horizontal - x) * 0.2, vertical + (vertical - y) * 0.2)

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
        y += Vy

    # drawing stuffs
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(x - 25, y - 25, 50, 50))
    for i in range(len(Fx)):
        drawForce(Fx[i], Fy[i])




    clock.tick(fps)
    pygame.display.flip()

pygame.quit()
