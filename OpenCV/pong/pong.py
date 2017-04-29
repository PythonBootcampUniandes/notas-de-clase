#!/usr/bin/env python

import os
import csv
import cv2
import glob
import pygame
import scipy.misc
import numpy as np
import scipy.io as sio
from pygame.locals import *
import pygame.camera as Camera
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

computer = True
finish = False
pygame.init()
h = 480
w = 640
size = (w,h)
SCR_WID, SCR_HEI = 640, 480
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pong')
ubuntu = pygame.font.match_font('Ubuntu')
font = pygame.font.Font(ubuntu, 13)
lastDelta = 0

red_lower = np.array([0, 150, 0],np.uint8)
red_upper = np.array([5, 255, 255],np.uint8)

blue_lower = np.array([110,50,50], np.uint8)
blue_upper = np.array([130,255,255], np.uint8)

Camera.init()
c = Camera.Camera(Camera.list_cameras()[0], size)
c.start()

def clear():
    os.system('clear')

class Player():
	def __init__(self):
		self.x, self.y = 16, SCR_HEI/2
		self.speed = 5
		self.padWid, self.padHei = 8, 64
		self.score = 0
		self.scoreFont = pygame.font.SysFont("calibri",40)
		self.lst = [self.y, 0]
	
	def scoring(self):
		scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
		screen.blit(scoreBlit, (32, 16))
		if self.score == 10:
			print "Player 1 wins!"
			exit()
	
	def movement(self, nY, com = computer, al = 4.5):		
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
	
		elif not com:
			now = self.delta(nY)
			if now < 0:
				self.y -= self.speed
			elif now > 0:
				self.y += self.speed
	
			if self.y <= 0:
				self.y = 0
			elif self.y >= SCR_HEI-64:
				self.y = SCR_HEI-64

	def delta(self, par):
		if self.lst[0] != par:
			self.lst[1], self.lst[0] = self.lst[0], par
		return self.lst[0] - self.lst[1]

	
	def draw(self):
		pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))

	

class Enemy():
	def __init__(self):
		self.x, self.y = SCR_WID-16, SCR_HEI/2
		self.speed = 5
		self.padWid, self.padHei = 8, 64
		self.score = 0
		self.scoreFont = pygame.font.SysFont("calibri",40)
		self.lst = [self.y, 0]
	
	def scoring(self):
		scoreBlit = self.scoreFont.render(str(self.score), 1, (255, 255, 255))
		screen.blit(scoreBlit, (SCR_HEI+92, 16))
		if self.score == 10:
			print "Player 2 wins!"
			exit()

	def delta(self, par):
		if self.lst[0] != par:
			self.lst[1], self.lst[0] = self.lst[0], par
		return self.lst[0] - self.lst[1]
	
	def movement(self, mY):
		#keys = pygame.key.get_pressed()
		now = self.delta(mY)
		if now < 0:
			self.y -= self.speed
		elif now > 0:
			self.y += self.speed
	
		if self.y <= 0:
			self.y = 0
		elif self.y >= SCR_HEI-64:
			self.y = SCR_HEI-64
	
	def draw(self):
		pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.padWid, self.padHei))

class Ball():
	def __init__(self):
		self.x, self.y = SCR_WID/2, SCR_HEI/2
		self.speed_x = -3
		self.speed_y = 3
		self.size = 8
	
	def movement(self):
		self.x += self.speed_x
		self.y += self.speed_y

		#wall col
		if self.y <= 0:
			self.speed_y *= -1
		elif self.y >= SCR_HEI-self.size:
			self.speed_y *= -1

		if self.x <= 0:
			self.__init__()
			enemy.score += 1
		elif self.x >= SCR_WID-self.size:
			self.__init__()
			self.speed_x = 3
			player.score += 1
		##wall col
		#paddle col
		#player
		for n in range(-self.size, player.padHei):
			if self.y == player.y + n:
				if self.x <= player.x + player.padWid:
					self.speed_x *= -1
					break
			n += 1
		#enemy
		for n in range(-self.size, enemy.padHei):
			if self.y == enemy.y + n:
				if self.x >= enemy.x - enemy.padWid:
					self.speed_x *= -1
					break
			n += 1
		##paddle col

	def draw(self):
		pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 8, 8))



def transposeImg(img):
    r, g, b = np.rollaxis(img[...,:3], axis = -1)
    return np.dstack([r.T, g.T, b.T])

def rgb2gray(rgb):
    r, g, b = np.rollaxis(rgb[...,:3], axis = -1)
    return 0.299 * r + 0.587 * g + 0.114 * b

def extractBlue(hsv):
    mask = cv2.inRange(hsv, blue_lower, blue_upper)
    blur = cv2.GaussianBlur(mask,(5,5),0)
    ret,thr = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _,contour1,hierarchy1 = cv2.findContours(thr,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt1 = maxArea(contour1)
    try:
      M1 = cv2.moments(cnt1)
      c1_x = int(M1['m10']/M1['m00'])
      c1_y = int(M1['m01']/M1['m00'])
    except Exception:
      c1_x = 0
      c1_y = 0
    return (c1_x, c1_y)

def extractRed(hsv):
    mask = cv2.inRange(hsv, red_lower, red_upper)
    blur = cv2.GaussianBlur(mask,(5,5),0)
    ret,thr = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _,contour1,hierarchy1 = cv2.findContours(thr,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnt1 = maxArea(contour1)
    try:
      M1 = cv2.moments(cnt1)
      c1_x = int(M1['m10']/M1['m00'])
      c1_y = int(M1['m01']/M1['m00'])
    except Exception:
      c1_x = 0
      c1_y = 0
    return (c1_x, c1_y)


def maxArea(contour):
    max_area = 0
    best_cnt = None
    for cnt in contour:
        area = cv2.contourArea(cnt)
        if area > 1000:
           if area > max_area:
              max_area = area
              best_cnt = cnt
    return best_cnt


clock = pygame.time.Clock()
FPS = 60
ball = Ball()
player = Player()
enemy = Enemy()
computer = True

while not finish:
  surf = c.get_image()
  img = np.flipud(pygame.surfarray.pixels3d(surf))
  img = transposeImg(img)
  hsv = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
  hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)
  c1_x,c1_y = extractRed(hsv)
  c2_x,c2_y = extractBlue(hsv)
  surf = pygame.surfarray.make_surface(np.flipud(np.flipud(transposeImg(img))))
  if not c1_x == 0 and not c1_y == 0:
     pygame.draw.circle(surf, [255, 0, 0], (c1_x, c1_y), 5)
  if not c2_x == 0 and not c2_y == 0:
     pygame.draw.circle(surf, [0, 0, 255], (c2_x, c2_y), 5)

  if c2_y != 0 and c1_y != 0:
     computer = False
  elif c2_y != 0 and c1_y == 0:
     computer = True

  print computer

  ball.movement()
  player.movement(c1_y, computer)
  enemy.movement(c2_y)
  screen.blit(surf, (0,0))
  #screen.fill((0, 0, 0))
  ball.draw()
  player.draw()
  player.scoring()
  enemy.draw()
  enemy.scoring()
  ##draw
  #_______
  pygame.display.flip()
  clock.tick(FPS)
  pygame.display.update()
  #clear()
  for event in pygame.event.get(): # User did something
      if event.type == pygame.QUIT: # If user clicked close
         finish = True

pygame.quit()
