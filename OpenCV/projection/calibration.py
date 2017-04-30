#!/usr/bin/env python

import cv2
import pygame
import numpy as np
from pygame.locals import *
# import pygame.camera as camera

FPS = 60

h, w = 480, 640
size = (w, h)
SCR_WID, SCR_HEI = size

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)


objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
images = []  # Calibration images
num_images = 10  # Required number of calibration images


def transposeImg(img):
    r, g, b = np.rollaxis(img[..., :3], axis=-1)
    return np.dstack([r.T, g.T, b.T])


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Calibration')

    ubuntu = pygame.font.match_font('Ubuntu')
    font = pygame.font.Font(ubuntu, 20)
    font.set_bold(True)
    cap = cv2.VideoCapture(0)

    # camera.init()
    # c = camera.Camera(camera.list_cameras()[0], size)
    # c.start()

    finish = False
    clock = pygame.time.Clock()
    total_images = 0

    while not finish and total_images < num_images:

        text = font.render('{0}/{1}'.format(total_images, num_images),
                           False, (255, 255, 0))
        textRect = text.get_rect()
        textRect.centerx = 60
        textRect.centery = 20

        # surf = c.get_image()
        # img = pygame.surfarray.pixels3d(surf)
        _, img = cap.read()
        # img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (6, 6), None)
        img_gray = np.dstack([gray, gray, gray])
        if ret:
            cv2.cornerSubPix(gray, corners, (12, 12), (-1, -1), criteria)
            cv2.drawChessboardCorners(img_gray, (6, 6), corners, ret)
        gray_surf = pygame.surfarray.make_surface(
            np.flipud(np.flipud(transposeImg(img_gray))))
        # gray_surf = pygame.surfarray.make_surface(img_gray)
        screen.blit(gray_surf, (0, 0))
        screen.blit(text, textRect)
        clock.tick(FPS)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            keys = pygame.key.get_pressed()
            if keys[K_SPACE] and ret:
                # images.append(img)
                objpoints.append(objp)
                imgpoints.append(corners)
                total_images += 1

    # c.stop()

    print("Calibrating camera....")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints,
                                                       gray.shape[::-1], None,
                                                       None)
    print("Saving calibration matrix...")
    np.savez('calib_camera.npz', ret=ret, mtx=mtx, dist=dist,
             rvecs=rvecs, tvecs=tvecs)


if __name__ == '__main__':
    main()
