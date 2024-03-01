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

    def add_force(self, Fx=tuple, Fy=tuple):
        self.Fx.append([Fx[0], Fx[1]])
        self.Fy.append([Fy[0], Fy[1]])

    def draw(self, surface):
        width = 32
        points = [(self.x + width * math.cos(self.theta), self.y + width * math.sin(self.theta)),
                  (self.x - width * math.sin(self.theta), self.y + width * math.cos(self.theta)),
                  (self.x - width * math.cos(self.theta), self.y - width * math.sin(self.theta)),
                  (self.x + width * math.sin(self.theta), self.y - width * math.cos(self.theta))]
        pygame.draw.polygon(surface, (100, 100, 100), points)


