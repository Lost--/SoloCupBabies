#!/usr/bin/python

import cv2
import numpy as np
import sys


def get_contours(img):
	lower = np.array([05, 05, 150], dtype ="uint8")
	upper = np.array([60, 60, 240], dtype="uint8")
	mask = cv2.inRange(img, lower, upper)
	output = cv2.bitwise_and(img, img, mask=mask)
	erode = cv2.erode(output, None, 15)
	dilate = cv2.dilate(output, None, 12)

	gray = cv2.cvtColor(dilate,cv2.COLOR_BGR2GRAY)
	thresh, im_bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	im_bw_copy = im_bw.copy()
	contours, hierarchy = cv2.findContours(im_bw_copy,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
	return contours


def get_largest_contour(contours):
	largest = None
	for i, cnt1 in enumerate(contours):
		x = i
		if largest is None or len(largest) < len(cnt1):
			largest = cnt1
	return largest

if __name__ == "__main__":
	img = cv2.imread(sys.argv[1])
	contours = get_contours(img)
	print contours
	largest = get_largest_contour(contours)
	cv2.drawContours(img, largest, -1, (255,0,0), 3)
	cv2.imshow("title", img)
	cv2.waitKey(0)
