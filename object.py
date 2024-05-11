from time import perf_counter
import pygame
from math import sin, cos
import numpy as np


class Object():
    def __init__(self, x, y, sizeX, sizeY, speedX=0, speedY=0, angle=0, turning_speed=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speedX = speedX
        self.speedY = speedY
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.time = perf_counter()
        self.color = (255, 255, 255)
        self.turning_speed = turning_speed

        self.push_off_the_walls = True

    def update(self):
        self.x += self.speedX * (perf_counter() - self.time)
        self.y += self.speedY * (perf_counter() - self.time)

        self.count_angles() # counting self.a, self.b, self.c, self.d
        l = [self.a, self.b, self.c, self.d]

        for i in l:
            if i[0] > screen.get_size()[0] or i[0] < 0:
                self.speedX *= -1
            if i[1] > screen.get_size()[1] or i[1] < 0:
                self.speedY *= -1

        self.angle += self.turning_speed * (perf_counter() - self.time)

        self.time = perf_counter()

    def pos(self):
        return np.array([self.x, self.y])

    def count_angles(self):
        d1 = np.array([cos(self.angle) * self.sizeX / 2, sin(self.angle) * self.sizeX / 2])
        d2 = np.array([-sin(self.angle) * self.sizeY / 2, cos(self.angle) * self.sizeY / 2])

        self.a = self.pos() - d1 - d2
        self.b = self.pos() + d1 - d2
        self.c = self.pos() + d1 + d2
        self.d = self.pos() - d1 + d2

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.a, self.b, 1)
        pygame.draw.line(screen, self.color, self.b, self.c, 1)
        pygame.draw.line(screen, self.color, self.c, self.d, 1)
        pygame.draw.line(screen, self.color, self.d, self.a, 1)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    obj1 = Object(500, 500, 200, 100, speedX=200, speedY=200, angle=20, turning_speed=.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))

        obj1.update()
        obj1.draw(screen)

        pygame.display.flip()