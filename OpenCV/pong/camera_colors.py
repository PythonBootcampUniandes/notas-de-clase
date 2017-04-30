#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pygame
import numpy as np
from pygame.locals import *
import pygame.camera as camera

FPS = 60

h, w = 480, 640
size = (w, h)


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Extracción de colores')

    camera.init()
    c = camera.Camera(camera.list_cameras()[0], size)
    c.start()

    finish = False
    clock = pygame.time.Clock()

    while not finish:
        surf = c.get_image()
        img = pygame.surfarray.pixels3d(surf)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        surf = pygame.surfarray.make_surface(hsv)
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
    c.stop()


if __name__ == '__main__':
    main()
