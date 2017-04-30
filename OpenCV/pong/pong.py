#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cv2
import pygame
import numpy as np
from pygame.locals import *
import pygame.camera as Camera


h = 480
w = 640

size = (w, h)
SCR_WID, SCR_HEI = 640, 480
lastDelta = 0
computer = True

finish = False
pygame.init()

Camera.init()
c = Camera.Camera(Camera.list_cameras()[0], size)
c.start()

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pong')
# ubuntu = pygame.font.match_font('Ubuntu')
# font = pygame.font.Font(ubuntu, 13)


def clear():
    os.system('clear')


class Player():
    def __init__(self):
        self.x, self.y = 16, SCR_HEI / 2
        self.speed = 5
        self.padWid, self.padHei = 8, 64
        self.score = 0
        self.scoreFont = pygame.font.SysFont("calibri", 40)
        self.lst = [self.y, 0]

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
        screen.blit(scoreBlit, (32, 16))
        if self.score == 10:
            print("Player 1 wins!")
            exit()

    def movement(self, nY, com=computer, al=4.5):
        if com:
            if ball.x < SCR_WID / al:
                if self.y <= 0:
                    self.y = 0
                elif self.y >= SCR_HEI - 64:
                    self.y = SCR_HEI - 64
                if self.y <= ball.y:
                    self.y += self.speed
                elif self.y > ball.y:
                    self.y -= self.speed
        else:
            now = self.delta(nY)
            if now < 0:
                self.y -= self.speed
            elif now > 0:
                self.y += self.speed

            if self.y <= 0:
                self.y = 0
            elif self.y >= SCR_HEI - 64:
                self.y = SCR_HEI - 64

    def delta(self, par):
        if self.lst[0] != par:
            self.lst[1], self.lst[0] = self.lst[0], par
        return self.lst[0] - self.lst[1]

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x, self.y, self.padWid, self.padHei))


class Enemy():
    def __init__(self):
        self.x, self.y = SCR_WID - 16, SCR_HEI / 2
        self.speed = 5
        self.padWid, self.padHei = 8, 64
        self.score = 0
        self.scoreFont = pygame.font.SysFont("calibri", 40)
        self.lst = [self.y, 0]

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
        screen.blit(scoreBlit, (SCR_HEI + 92, 16))
        if self.score == 10:
            print("Player 2 wins!")
            exit()

    def delta(self, par):
        if self.lst[0] != par:
            self.lst[1], self.lst[0] = self.lst[0], par
        return self.lst[0] - self.lst[1]

    def movement(self, mY):
        # keys = pygame.key.get_pressed()
        # now = self.delta(mY)
        self.y = mY
        # if now < 0:
        #   self.y -= self.speed
        # elif now > 0:
        #   self.y += self.speed
        if self.y <= 0:
            self.y = 0
        elif self.y >= SCR_HEI - 64:
            self.y = SCR_HEI - 64

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255),
                         (self.x, self.y, self.padWid, self.padHei))


class Ball():
    def __init__(self):
        self.x, self.y = SCR_WID / 2, SCR_HEI / 2
        self.speed_x = -6
        self.speed_y = 6
        self.size = 8

    def movement(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # wall col
        if self.y <= 0:
            self.speed_y *= -1
        elif self.y >= SCR_HEI - self.size:
            self.speed_y *= -1

        if self.x <= 0:
            self.__init__()
            enemy.score += 1
        elif self.x >= SCR_WID - self.size:
            self.__init__()
            self.speed_x = 3
            player.score += 1
        # wall col
        # paddle col
        # player
        for n in range(-self.size, player.padHei):
            if self.y == player.y + n:
                if self.x <= player.x + player.padWid:
                    self.speed_x *= -1
                    break
            n += 1
        # enemy
        for n in range(-self.size, enemy.padHei):
            if self.y == enemy.y + n:
                if self.x >= enemy.x - enemy.padWid:
                    self.speed_x *= -1
                    break
            n += 1
        # paddle col

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 8, 8))


def transposeImg(img):
    r, g, b = np.rollaxis(img[..., :3], axis=-1)
    return np.dstack([r.T, g.T, b.T])


def find_max_contour(contours):
    max_cnt, max_area = None, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_cnt, max_area = cnt, area
    return max_cnt


def threshold_object_color(img, lower_color, upper_color):
    c_x, c_y = 0, 0  # Coordenadas del centroide
    try:
        # Escribir el código aquí
        mask = cv2.inRange(img, lower_color, upper_color)
        orig_mask = mask.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        morph_mask = mask.copy()
        _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)
        # print(len(contours))

        max_cnt = find_max_contour(contours)
        moments = cv2.moments(max_cnt)
        c_x = moments['m10'] // moments['m00']
        c_y = moments['m01'] // moments['m00']
        # print("Implementar")
    except Exception:
        pass
    return int(c_x), int(c_y), orig_mask, morph_mask


clock = pygame.time.Clock()
FPS = 60
ball = Ball()
player = Player()
enemy = Enemy()


def draw_pong(threshold_func):
    global finish
    c1_x, c1_y = (0, 0)
    while not finish:
        surf = c.get_image()
        img = np.flipud(pygame.surfarray.pixels3d(surf))
        img = transposeImg(img)
        hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        c2_x, c2_y = threshold_func(hsv)
        surf = pygame.surfarray.make_surface(
            np.flipud(np.flipud(transposeImg(img))))
        if not c1_x == 0 and not c1_y == 0:
            pygame.draw.circle(surf, [255, 0, 0], (c1_x, c1_y), 5)
        if not c2_x == 0 and not c2_y == 0:
            pygame.draw.circle(surf, [0, 255, 0], (c2_x, c2_y), 5)

        if c2_y != 0 and c1_y != 0:
            computer = False
        elif c2_y != 0 and c1_y == 0:
            computer = True

        ball.movement()
        player.movement(c1_y, computer)
        enemy.movement(c2_y)
        screen.blit(surf, (0, 0))
        ball.draw()
        player.draw()
        player.scoring()
        enemy.draw()
        enemy.scoring()

        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                finish = True

    pygame.quit()
