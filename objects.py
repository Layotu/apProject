import pygame
import math

import draw

font = pygame.font.SysFont("Jetbrains Mono", 15)


class Body:
    x = 0
    y = 0
    Vx = 0
    Vy = 0

    # [[X0, Xf]]
    Fx = []
    Fy = []
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
        for i in self.Fx:
            self.Vx += (i[1] - i[0]) / self.mass
        for i in self.Fy:
            self.Vy += (i[1] - i[0]) / self.mass

        if friction:
            self.Vx -= max(self.mu * self.mass, 0) * (self.Vx / max(abs(self.Vx), 0.01))
            self.Vy -= max(self.mu * self.mass, 0) * (self.Vy / max(abs(self.Vy), 0.01))

        self.x += self.Vx
        self.y -= self.Vy

        # torques (apparently I hate myself and enjoy suffering)
        self.theta += self.w

    def add_force(self, Fx, Fy):
        self.Fx.append([Fx[0], Fx[1]])
        self.Fy.append([Fy[0], Fy[1]])

    def update_force(self, index, Fx=tuple, Fy=tuple):
        self.Fx[index] = ([Fx[0], Fx[1]])
        self.Fy[index] = ([Fy[0], Fy[1]])

    def draw(self, surface):
        width = (self.mass ** 0.3333) * 8
        points = [(self.x + width * math.cos(self.theta), self.y + width * math.sin(self.theta)),
                  (self.x - width * math.sin(self.theta), self.y + width * math.cos(self.theta)),
                  (self.x - width * math.cos(self.theta), self.y - width * math.sin(self.theta)),
                  (self.x + width * math.sin(self.theta), self.y - width * math.cos(self.theta))]
        pygame.draw.polygon(surface, (100, 100, 100), points)

        coords = font.render("X: " + str(round(self.x * 100) / 100.0) + " Y: " + str(round(self.y * 100) / 100.0) + "θ: " + str(self.theta - math.pi / 4), True, 0)
        kinematics = font.render("Speed: " + str(round(math.sqrt(self.Vx ** 2 + self.Vy ** 2) * 100) / 100.0) + " Mass: " + str(round(self.mass * 100) / 100.0), True, 0)
        k = round(0.5 * self.mass * (self.Vx ** 2 + self.Vy ** 2)) / 10.0
        ug = round(self.mass * .1 * (surface.get_height() - self.y - width)) / 10.0
        energy = font.render("K: " + str(k) + " Ug: " + str(ug) + " Net: " + str(round(k + ug * 10) / 10), True, 0)
        surface.blit(coords, (self.x - width, self.y - width - 20))
        surface.blit(kinematics, (self.x - width, self.y - width - 10))
        surface.blit(energy, (self.x - width, self.y - width))

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

        self.Vx += (.002 * mass * self.mass / max(r, 1) * math.cos(theta)) / self.mass
        self.Vy += (.002 * mass * self.mass / max(r, 1) * math.sin(theta)) / self.mass

        if mass / max(r, 0.1) > 0.02:
            Fx = max(min(mass * self.mass / max(r, 0.1) * math.cos(theta), 8), -8)
            Fy = max(min(mass * self.mass / max(r, 0.1) * math.sin(theta), 8), -8)
            draw.draw_vector(screen, Fx, Fy, self.x, self.y, (0, 100, 0))

    def calc_collision(self, surface, other):
        if abs(other.x - self.x) < (self.mass ** 0.3333 * 6 + other.mass ** 0.3333 * 4) and abs(other.y - self.y) < self.mass ** 0.3333 * 6 + other.mass ** 0.3333 * 4:
            pX = self.mass * self.Vx
            pY = self.mass * self.Vy
            pX1 = other.mass * other.Vx
            pY1 = other.mass * other.Vy
            avgX = (pX + pX1) / 2
            avgY = (pY + pY1) / 2

            self.Vx = (pX1 + avgX) / self.mass / 2
            self.Vy = (pY1 + avgY) / self.mass / 2

            if other.y + other.mass ** 0.3333 * 8 > surface.get_height():
                self.Vy = min(self.Vx - .98, 1)
            elif other.y + other.mass ** 0.3333 * 4 < 0:
                self.Vy -= 0.73

            elif other.x + other.mass ** 0.3333 * 4 > surface.get_width():
                self.Vx += 0.73
            elif other.x + other.mass ** 0.3333 * 4 < 0:
                self.Vx -= 0.73

            else:
                other.Vx = (pX + avgX) / other.mass / 2
                other.Vy = (pY + avgY) / other.mass / 2

            self.step()
            other.step()

    def wall_collision(self, screen):
        if self.y + self.mass ** 0.3333 * 8 > screen.get_height():
            draw.draw_vector(screen, 0, 8 * (1 - self.Vy) * 0.5, self.x, self.y, (0, 0, 100))
            self.Vy = (1 - self.Vy) * 0.5
            self.y = screen.get_height() - self.mass ** 0.3333 * 4
        if self.y + self.mass ** 0.3333 * 4 < 0:
            draw.draw_vector(screen, 0, 8 * (-1 - self.Vy) * 0.5, self.x, self.y, (0, 0, 100))
            self.Vy = (-1 - self.Vy) * 0.5
            self.y = -self.mass ** 0.3333 * 4

        if self.x + self.mass ** 0.3333 * 4 > screen.get_width():
            draw.draw_vector(screen, 8 * (1 - self.Vx) * 0.5, 0, self.x, self.y, (0, 0, 100))
            self.Vx = (1 - self.Vx) * 0.5
            self.x = screen.get_width() - self.mass ** 0.3333 * 4
        if self.x + self.mass ** 0.3333 * 4 < 0:
            draw.draw_vector(screen, 8 * (-1 - self.Vx), 0, self.x, self.y, (0, 0, 100))
            self.Vx = (-1 - self.Vx) * 0.5
            self.x = -self.mass ** 0.3333 * 4

class StaticMass:
    pass
