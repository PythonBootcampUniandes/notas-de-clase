#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pong
import numpy as np


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
        # orig_mask = mask.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        # morph_mask = mask.copy()
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
    return int(c_x), int(c_y)


def main():
    hsv_color = np.array([[[12, 255, 255]]])
    h, s, v = hsv_color[0, 0]

    lower_color = np.array([[[-10 + h, 230, 100]]])
    upper_color = hsv_color + np.array([[[0 + h, 255, 255]]])

    lower_color = lower_color[:, 0]
    upper_color = upper_color[:, 0]

    pong.draw_pong(lambda x: threshold_object_color(x,
                                                    lower_color,
                                                    upper_color))


if __name__ == '__main__':
    main()
