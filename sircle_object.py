from math import pi
from random import randint, uniform
from time import perf_counter
import numpy as np
import pygame

import utils


class SircleObject:
    def __init__(self, x, y, r, speedX=0, speedY=0):
        self.x = x
        self.y = y
        self.speedX = speedX
        self.speedY = speedY
        self.r = r
        self.time = perf_counter()
        self.color = (255, 255, 255)

        self.push_off_the_walls = True

    def update(self, screen):
        self.x += self.speedX * (perf_counter() - self.time)
        self.y += self.speedY * (perf_counter() - self.time)

        if self.x + self.r > screen.get_size()[0]:
            self.speedX = -abs(self.speedX)
        if self.x - self.r < 0:
            self.speedX = abs(self.speedX)

        if self.y + self.r > screen.get_size()[1]:
            self.speedY = -abs(self.speedY)
        if self.y - self.r < 0:
            self.speedY = abs(self.speedY)

        self.time = perf_counter()

    def pos(self):
        return np.array([self.x, self.y])


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos(), self.r, 1)

    def collision(self, objects):
        for obj in objects:
            if self != obj and utils.dist(self.pos(), obj.pos()) < (obj.r + self.r):
                self.color = (255, 0, 0)
                break
        else:
            self.color = (0, 255, 0)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    objects = [SircleObject(randint(0, screen.get_size()[0]), randint(0, screen.get_size()[1]),
                      randint(10, 50), speedX=randint(0, 400), speedY=randint(0, 400)) for _ in range(20)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))

        for obj in objects:
            obj.update(screen)
            obj.draw(screen)
            obj.collision(objects)

        pygame.display.flip()