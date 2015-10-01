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
	cv2.drawContours(img, contours, -1, (255,0,0), 3)
	cv2.imshow("title", img)
	cv2.waitKey(0)
	return contours, thresh

def find_if_close(cnt1,cnt2):
	row1,row2 = cnt1.shape[0],cnt2.shape[0]
	for i in xrange(row1):
		for j in xrange(row2):
			dist = np.linalg.norm(cnt1[i]-cnt2[j])
			if abs(dist) < 50 :
				return True
			elif i==row1-1 and j==row2-1:
				return False

def cluster_contours(contours):
	LENGTH = len(contours)
	status = np.zeros((LENGTH,1))
	for i,cnt1 in enumerate(contours):
		x = i    
		if i != LENGTH-1:
			for j,cnt2 in enumerate(contours[i+1:]):
				x = x+1
				dist = find_if_close(cnt1,cnt2)
				if dist == True:
					val = min(status[i],status[x])
					status[x] = status[i] = val
				else:
					if status[x]==status[i]:
						status[x] = i+1
	return status

if __name__ == "__main__":
	img = cv2.imread(sys.argv[1])
	contours, thresh = get_contours(img)
	#print contours 
	status = cluster_contours(contours)
	unified = []
	maximum = int(status.max())+1
	for i in xrange(maximum):
		pos = np.where(status==i)[0]
		if pos.size != 0:
			cont = np.vstack(contours[i] for i in pos)
			hull = cv2.convexHull(cont)
			unified.append(hull)
	cv2.drawContours(img,unified,-1,(0,255,0),2)
	cv2.drawContours(thresh,unified,-1,255,-1)
