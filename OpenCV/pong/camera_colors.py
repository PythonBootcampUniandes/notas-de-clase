#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pygame
import numpy as np
from pygame.locals import *

FPS = 60

h, w = 480, 640
size = (w, h)


def transposeImg(img):
    r, g, b = np.rollaxis(img[..., :3], axis=-1)
    return np.dstack([r.T, g.T, b.T])


def threshold_object_color(img, lower_color, upper_color):
    c_x, c_y = 0, 0  # Coordenadas del centroide
    try:
        # Escribir el código aquí
        print("Implementar")
    except Exception:
        pass
    return c_x, c_y


def main():
    # Definir rangos de colores
    hsv_color = np.array([[[12, 255, 255]]])
    h, s, v = hsv_color[0, 0]

    lower_color = np.array([[[-10 + h, 230, 100]]])
    upper_color = hsv_color + np.array([[[0 + h, 255, 255]]])

    lower_color = lower_color[:, 0]
    upper_color = upper_color[:, 0]

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Camera Pong')

    # camera.init()
    # c = camera.Camera(camera.list_cameras()[0], size)
    # c.start()

    finish = False
    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0)

    while not finish:
        _, img = cap.read()
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        c_x, c_y = threshold_object_color(hsv,
                                                lower_color,
                                                upper_color)
        surf = pygame.surfarray.make_surface(np.flipud(
            np.flipud(transposeImg(img))))
        if (c_x, c_y) != (None, None):
            pygame.draw.circle(surf, [0, 255, 0], (int(c_x), int(c_y)), 5)
        screen.blit(surf, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
    # c.stop()


if __name__ == '__main__':
    main()
