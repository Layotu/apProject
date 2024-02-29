import pygame
import math

pygame.init()
pygame.font.init()


# function for drawing arrows for the velocity and force vectors
def draw_vector(screen, horizontal, vertical, x, y, color=(0, 0, 0)):
    if horizontal + vertical == 0:
        return
    pygame.draw.aaline(screen, color, (x, y), (x + horizontal * 8, y - vertical * 8))
    theta = math.atan2(vertical, horizontal)
    pygame.draw.aaline(screen, color, (x + horizontal * 8, y - vertical * 8), (x + horizontal * 8 - max(math.sqrt(horizontal**2 + vertical**2), 8) * math.cos(theta + 0.5), y - vertical * 8 + max(math.sqrt(horizontal**2 + vertical**2), 8) * math.sin(theta + 0.5)))
    pygame.draw.aaline(screen, color, (x + horizontal * 8, y - vertical * 8), (x + horizontal * 8 - max(math.sqrt(horizontal**2 + vertical**2), 8) * math.cos(theta - 0.5), y - vertical * 8 + max(math.sqrt(horizontal**2 + vertical**2), 8) * math.sin(theta - 0.5)))


# draw the UI
def display_ui(screen):
    font = pygame.font.SysFont("Jetbrains Mono", 30)

    pygame.draw.rect(screen, (119, 136, 153), pygame.Rect(screen.get_width() * 0.75, 0, screen.get_width() * 0.25, screen.get_height()))

    # 'add new force' button
    pygame.draw.rect(screen, (200, 100, 20), pygame.Rect(screen.get_width() * 0.775, screen.get_height() * 0.025, screen.get_width() * 0.2, screen.get_height() * 0.15))
    text = font.render("Add new force", True, 0)
    screen.blit(text, (screen.get_width() * 0.82, screen.get_height() * 0.085))

    # 'delete selected force' button
    pygame.draw.rect(screen, (200, 100, 20), pygame.Rect(screen.get_width() * 0.775, screen.get_height() * 0.225, screen.get_width() * 0.2, screen.get_height() * 0.15))
    text = font.render("Delete selected force", True, 0)
    screen.blit(text, (screen.get_width() * 0.795, screen.get_height() * 0.285))

    # 'Toggle orbit mode' button
    pygame.draw.rect(screen, (200, 100, 20), pygame.Rect(screen.get_width() * 0.775, screen.get_height() * 0.425, screen.get_width() * 0.2, screen.get_height() * 0.15))
    text = font.render("Toggle orbit mode", True, 0)
    screen.blit(text, (screen.get_width() * 0.805, screen.get_height() * 0.485))

    # unused button
    pygame.draw.rect(screen, (200, 100, 20), pygame.Rect(screen.get_width() * 0.775, screen.get_height() * 0.625, screen.get_width() * 0.2, screen.get_height() * 0.15))
    text = font.render("", True, 0)
    screen.blit(text, (screen.get_width() * 0.8, screen.get_height() * 0.685))

    # 'Reset' button
    pygame.draw.rect(screen, (200, 100, 20), pygame.Rect(screen.get_width() * 0.775, screen.get_height() * 0.825, screen.get_width() * 0.2, screen.get_height() * 0.15))
    text = font.render("Reset", True, 0)
    screen.blit(text, (screen.get_width() * 0.85, screen.get_height() * 0.885))


# draw the player
def draw_player(surface, x, y, theta):
    width = 32
    points = [(x + width * math.cos(theta), y + width * math.sin(theta)),
              (x - width * math.sin(theta), y + width * math.cos(theta)),
              (x - width * math.cos(theta), y - width * math.sin(theta)),
              (x + width * math.sin(theta), y - width * math.cos(theta))]
    pygame.draw.polygon(surface, (100, 100, 100), points)