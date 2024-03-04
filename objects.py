import pygame
import math

import draw


class Body:
    x = 0
    y = 0
    Vx = 0.01
    Vy = 0.01

    # [[X0, Xf]]
    Fx = []
    Fy = []
    mass = 4
    mu = 0.008

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

        self.Vx -= self.mu * (self.Vx / max(abs(self.Vx), 0.1)) * self.mass
        self.Vy -= self.mu * (self.Vy / max(abs(self.Vy), 0.1)) * self.mass

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
        width = (self.mass ** 0.5) * 4
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
        pygame.draw.aaline(screen, (100, 0, 0), (self.x + dX * 8, self.y - dY * 8), (self.x + dX * 8 - max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.cos(theta + 0.5), self.y - dY * 8 + max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.sin(theta + 0.6)))
        pygame.draw.aaline(screen, (100, 0, 0), (self.x + dX * 8, self.y - dY * 8), (self.x + dX * 8 - max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.cos(theta - 0.5), self.y - dY * 8 + max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.sin(theta - 0.6)))

    def calc_gravity(self, screen, x, y, mass):
        dX = x - self.x
        dY = y - self.y
        r = math.sqrt(dX * dX + dY * dY)
        theta = math.atan2(-dY, dX)

        self.Vx += .008 * mass * self.mass / max(r, 1) * math.cos(theta)
        self.Vy += .008 * mass * self.mass / max(r, 1) * math.sin(theta)

        if mass / max(r, 0.1) > 3:
            Fx = max(min(4 * mass * self.mass / max(r, 0.1) * math.cos(theta), 8), -8)
            Fy = max(min(4 * mass * self.mass / max(r, 0.1) * math.sin(theta), 8), -8)
            draw.draw_vector(screen, Fx, Fy, self.x, self.y, (0, 100, 0))

    def calc_collision(self, screen, other):
        if abs(other.x - self.x) < self.mass ** 0.5 * 3 + other.mass ** 0.5 * 2 and abs(other.y - self.y) < self.mass ** 0.5 * 3 + other.mass ** 0.5 * 2:
            pX = self.mass * self.Vx
            pY = self.mass * self.Vy
            pX1 = other.mass * other.Vx
            pY1 = other.mass * other.Vy

            self.Vx = pX1 / self.mass
            self.Vy = pY1 / self.mass
            other.Vx = pX / other.mass
            other.Vy = pY / other.mass

            self.step()
            other.step()



class StaticMass:
    pass
