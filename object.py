from time import perf_counter
import pygame
from math import sin, cos, pi
from random import randint, uniform
import numpy as np
import utils


class Object():
    def __init__(self, x, y, sizeX, sizeY, speedX=0, speedY=0, angle=0, turning_speed=0.0):
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

        self.count_angles()

    def update(self, objects=None):
        self.x += self.speedX * (perf_counter() - self.time)
        self.y += self.speedY * (perf_counter() - self.time)

        self.count_angles() # counting self.a, self.b, self.c, self.d

        if self.push_off_the_walls:
            l = [self.a, self.b, self.c, self.d]
            for i in l:
                if i[0] < 0:
                    self.speedX = abs(self.speedX)
                elif i[0] > screen.get_size()[0]:
                    self.speedX = -abs(self.speedX)

                if i[1] < 1:
                    self.speedY = abs(self.speedY)
                elif i[1] > screen.get_size()[1]:
                    self.speedY = -abs(self.speedY)

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

    def collision(self, objects):
        for obj in objects:
            if self != obj and utils.rect_intersection(self.a, self.b, self.c, self.d, obj.a, obj.b, obj.c, obj.d):
                self.color = (255, 0, 0)
                break
        else:
            self.color = (0, 255, 0)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    objects = [Object(randint(0, screen.get_size()[0]), randint(0, screen.get_size()[1]),
                      randint(20, 100), randint(20, 100), speedX=randint(0, 400), speedY=randint(0, 400),
                      angle=0, turning_speed=uniform(0, pi)) for _ in range(10)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))

        for obj in objects:
            obj.update()
            obj.draw(screen)
            obj.collision(objects)

        pygame.display.flip()