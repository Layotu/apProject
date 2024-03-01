import pygame
import math


class Body:
    x = 0
    y = 0
    Vx = 0
    Vy = 0

    # [[X0, Xf]]
    Fx = []
    Fy = []
    mass = 4

    theta = math.pi / 4
    w = 0

    selected = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def step(self):
        # kinematics stuff to update values
        for i in self.Fx:
            self.Vx += (i[1] - i[0]) / self.mass
        for i in self.Fy:
            self.Vy += (i[1] - i[0]) / self.mass

        self.x += self.Vx
        self.y -= self.Vy

        # torques (apparently I hate myself and enjoy suffering)
        self.theta += self.w

    def add_force(self, Fx=tuple, Fy=tuple):
        self.Fx.append([Fx[0], Fx[1]])
        self.Fy.append([Fy[0], Fy[1]])

    def update_force(self, index, Fx=tuple, Fy=tuple):
        self.Fx[index] = ([Fx[0], Fx[1]])
        self.Fy[index] = ([Fy[0], Fy[1]])

    def draw(self, surface):
        width = self.mass ** (3/2) * 4
        points = [(self.x + width * math.cos(self.theta), self.y + width * math.sin(self.theta)),
                  (self.x - width * math.sin(self.theta), self.y + width * math.cos(self.theta)),
                  (self.x - width * math.cos(self.theta), self.y - width * math.sin(self.theta)),
                  (self.x + width * math.sin(self.theta), self.y - width * math.cos(self.theta))]
        pygame.draw.polygon(surface, (100, 100, 100), points)

    def draw_force(self, screen, index):
        dX = self.Fx[index][1] - self.Fx[index][0]
        dY = self.Fy[index][1] - self.Fy[index][0]
        pygame.draw.aaline(screen, (100, 0, 0), (self.x, self.y), (self.x + dX * 8, self.y - dY * 8))
        theta = math.atan2(dY, dX)
        pygame.draw.aaline(screen, (100, 0, 0), (self.x + dX * 8, self.y - dY * 8), (self.x + dX * 8 - max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.cos(theta + 0.5), self.y - dY * 8 + max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.sin(theta + 0.5)))
        pygame.draw.aaline(screen, (100, 0, 0), (self.x + dX * 8, self.y - dY * 8), (self.x + dX * 8 - max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.cos(theta - 0.5), self.y - dY * 8 + max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.sin(theta - 0.5)))
