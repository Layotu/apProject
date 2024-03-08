import pygame
import math

from pygame.math import *

import draw

font = pygame.font.SysFont("Jetbrains Mono", 15)


class Body:
    x = 0
    y = 0
    Vx = 0
    Vy = 0

    forces = [Vector2(0, -.98)]
    other_forces = []
    mass = 4
    mu = 0.006

    theta = math.pi / 4
    w = 0

    selected = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def step(self, friction=True):
        # kinematics stuff to update values
        self.Vx += self.net_force().x
        self.Vy += self.net_force().y

        if friction:
            self.Vx -= max(self.mu * self.mass, 0) * (self.Vx / max(abs(self.Vx), 0.01))
            self.Vy -= max(self.mu * self.mass, 0) * (self.Vy / max(abs(self.Vy), 0.01))

        self.x += self.Vx
        self.y -= self.Vy

        self.other_forces = []

        # torques (apparently I hate myself and enjoy suffering)
        self.theta += self.w

    def add_force(self, Fx, Fy):
        self.forces.append(Vector2(Fx, Fy))

    def update_force(self, index, Fx, Fy):
        self.forces.append(Vector2(Fx, Fy))

    def draw(self, surface):
        width = (self.mass ** 0.3333) * 8
        points = [(self.x + width * math.cos(self.theta), self.y + width * math.sin(self.theta)),
                  (self.x - width * math.sin(self.theta), self.y + width * math.cos(self.theta)),
                  (self.x - width * math.cos(self.theta), self.y - width * math.sin(self.theta)),
                  (self.x + width * math.sin(self.theta), self.y - width * math.cos(self.theta))]
        pygame.draw.polygon(surface, (100, 100, 100), points)

        coords = font.render("X: " + str(round(self.x * 100) / 100.0) + " Y: " + str(round(self.y * 100) / 100.0) + " θ: " + str(self.theta - math.pi / 4), True, 0)
        kinematics = font.render("Speed: " + str(round(math.sqrt(self.Vx ** 2 + self.Vy ** 2) * 100) / 100.0) + " Mass: " + str(round(self.mass * 100) / 100.0), True, 0)
        k = round(0.5 * self.mass * (self.Vx ** 2 + self.Vy ** 2)) / 10.0
        ug = round(self.mass * .1 * (surface.get_height() - self.y - width)) / 10.0
        energy = font.render("K: " + str(k) + " Ug: " + str(ug) + " Net: " + str(round(k + ug * 10) / 10), True, 0)
        #surface.blit(coords, (self.x - width, self.y - width - 20))
        #surface.blit(kinematics, (self.x - width, self.y - width - 10))
        #surface.blit(energy, (self.x - width, self.y - width))

    def draw_force(self, screen, index):
        dX = self.forces[index].x
        dY = self.forces[index].y
        pygame.draw.aaline(screen, (100, 0, 0), (self.x, self.y), (self.x + dX * 8, self.y - dY * 8))
        theta = math.atan2(dY, dX)
        pygame.draw.aaline(screen, (100, 0, 0), (self.x + dX * 8, self.y - dY * 8), (self.x + dX * 8 - max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.cos(theta + 0.5), self.y - dY * 8 + max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.sin(theta + 0.6)))
        pygame.draw.aaline(screen, (100, 0, 0), (self.x + dX * 8, self.y - dY * 8), (self.x + dX * 8 - max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.cos(theta - 0.5), self.y - dY * 8 + max(math.sqrt(dX ** 2 + dY ** 2), 8) * math.sin(theta - 0.6)))

    def calc_gravity(self, screen, x, y, mass):
        dX = x - self.x
        dY = y - self.y
        r = math.sqrt(dX * dX + dY * dY)
        theta = math.atan2(-dY, dX)

        self.Vx += (.2 * mass * self.mass / max(r, 1) * math.cos(theta)) / self.mass
        self.Vy += (.2 * mass * self.mass / max(r, 1) * math.sin(theta)) / self.mass

        if mass / max(r, 0.1) > 0.02:
            Fx = max(min(mass * self.mass / max(r, 0.1) * math.cos(theta), 8), -8)
            Fy = max(min(mass * self.mass / max(r, 0.1) * math.sin(theta), 8), -8)
            draw.draw_vector(screen, Fx, Fy, self.x, self.y, (0, 100, 0))

    def overlaps_with(self, other):
        x = abs(other.x - self.x) < (self.mass ** 0.3333 * 6 + other.mass ** 0.3333 * 4) + 4
        y = abs(other.y - self.y) < (self.mass ** 0.3333 * 6 + other.mass ** 0.3333 * 4) + 4
        return x and y

    def calc_collision(self, surface, other):
        if self.overlaps_with(other):

            pX = self.mass * self.Vx
            pY = self.mass * self.Vy
            pX1 = other.mass * other.Vx
            pY1 = other.mass * other.Vy
            avgX = (pX + pX1) / 2
            avgY = (pY + pY1) / 2

            if other.border_normal(surface).magnitude() == 0 and self.border_normal(surface).magnitude() == 0:
                self.other_forces.append(other.net_force())

            elif self.border_normal(surface).magnitude() == 0:
                self.other_forces.append(other.border_normal(surface))
                dist = other.mass ** 0.3333 * 8 + self.mass ** 0.3333 * 8
                self.x = min(max(dist, self.x), other.x - dist)
                self.y = min(max(dist, self.y), other.y - dist)

            self.step()
            other.step()

    def wall_collision(self, screen):
        width = self.mass ** 0.3333 * 4

        draw.draw_vector(screen, self.border_normal(screen).x * 4, self.border_normal(screen).y * 4, self.x, self.y, (0, 0, 100))
        self.Vx += self.border_normal(screen).x
        self.Vy += self.border_normal(screen).y
        self.x = min(max(width, self.x), screen.get_width() - width)
        self.y = min(max(width, self.y), screen.get_height() - width)

    def border_normal(self, screen):
        width = self.mass ** 0.3333 * 4
        normal = Vector2()

        if not width < self.x < screen.get_height() - width:
            normal.x = -1
        if not width < self.y < screen.get_height() - width:
            normal.y = -1
        normal = normal.elementwise() * self.net_force()
        normal += Vector2(max(self.x + width - screen.get_width(), 0), max(self.y + width - screen.get_height(), 0))
        return normal

    def net_force(self):
        net = Vector2()
        for force in self.forces:
            net += force
        for force in self.other_forces:
            net += force
        return net

    def calc_normal(self, surface):
        width = self.mass ** 0.3333 * 8
        normal = Vector2()
        if not width < self.x < surface.get_width() - width:
            normal[0] = -1.2
        if not width < self.y < surface.get_height() - width:
            normal[1] = -1.2

        normal *= self.net_force()
        return normal
