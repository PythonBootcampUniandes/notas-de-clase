#!/usr/bin/env python

import cv2
import pygame
import numpy as np
from pygame.locals import *
# import pygame.camera as camera

FPS = 240

h, w = 480, 640
size = (w, h)


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((6 * 6, 3), np.float32)
objp[:, :2] = np.mgrid[0:6, 0:6].T.reshape(-1, 2)


axis = np.float32([[0, 0, 0], [0, 3, 0], [3, 3, 0], [3, 0, 0],
                   [0, 0, -3], [0, 3, -3], [3, 3, -3], [3, 0, -3]])


def transposeImg(img):
    r, g, b = np.rollaxis(img[..., :3], axis=-1)
    return np.dstack([r.T, g.T, b.T])


def draw(img, corners, imgpts):
    imgpts = np.int32(imgpts).reshape(-1, 2)

    # draw ground floor in green
    img = cv2.drawContours(img, [imgpts[:4]], -1, (0, 255, 0), -3)

    # draw pillars in blue color
    for i, j in zip(range(4), range(4, 8)):
        img = cv2.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)

    # draw top layer in red color
    img = cv2.drawContours(img, [imgpts[4:]], -1, (0, 0, 255), 3)

    return img


def main():
    print("Loading calibration matrix....")

    with np.load('calib_camera.npz') as fp:
        mtx, dist = [fp[i] for i in ('mtx', 'dist')]

    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Calibration')

    ubuntu = pygame.font.match_font('Ubuntu')
    font = pygame.font.Font(ubuntu, 20)
    font.set_bold(True)

    # camera.init()
    # c = camera.Camera(camera.list_cameras()[0], size)
    # c.start()
    cap = cv2.VideoCapture(0)

    finish = False
    clock = pygame.time.Clock()

    while not finish:
        # surf = c.get_image()
        # img = pygame.surfarray.pixels3d(surf)
        # img = pygame.surfarray.pixels3d(surf)
        _, img = cap.read()
        # img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 6), None)
        img_gray = np.dstack([gray, gray, gray])
        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11),
                                        (-1, -1), criteria)
            _, rvecs, tvecs = cv2.solvePnP(objp, corners2,
                                           mtx, dist)
            # print(rvecs.shape)
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            img_gray = draw(img_gray, corners2, imgpts)

        # gray_surf = pygame.surfarray.make_surface(img_gray)
        gray_surf = pygame.surfarray.make_surface(
            np.flipud(np.flipud(transposeImg(img_gray))))
        screen.blit(gray_surf, (0, 0))
        clock.tick(FPS)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True

    # c.stop()


if __name__ == '__main__':
    main()
