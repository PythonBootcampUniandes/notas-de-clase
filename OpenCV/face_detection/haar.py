#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pygame
import numpy as np
from pygame.locals import *
# import pygame.camera as camera

FPS = 60

h, w = 480, 640
size = (w, h)

FRONTAL_FACE = 'haarcascades/haarcascade_frontalface_default.xml'


def transposeImg(img):
    r, g, b = np.rollaxis(img[..., :3], axis=-1)
    return np.dstack([r.T, g.T, b.T])


def face_detection(img):
    face_cascade = cv2.CascadeClassifier(FRONTAL_FACE)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h),
                      (0, 255, 0), 2)
    return img


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Haar cascades')

    # camera.init()
    # c = camera.Camera(camera.list_cameras()[0], size)
    # c.start()

    finish = False
    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0)

    while not finish:
        # surf = c.get_image()
        # img = np.flipud(pygame.surfarray.pixels3d(surf))
        # img = transposeImg(img)
        _, img = cap.read()
        # img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = face_detection(img)
        surf = pygame.surfarray.make_surface(np.flipud(
            np.flipud(transposeImg(img))))
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
