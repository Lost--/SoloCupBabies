#!/usr/bin/python

import cv2 
import numpy as np
import sys

def red_image(argv):
  img = cv2.imread(argv[1])
  lower = np.array([10, 10, 150], dtype ="uint8")
  upper = np.array([60, 60, 250], dtype="uint8")
  mask = cv2.inRange(img, lower, upper)
  output = cv2.bitwise_and(img, img, mask=mask)
  erode = cv2.erode(output, None, 15)
  dilate = cv2.dilate(output, None, 12)

  gray = cv2.cvtColor(dilate,cv2.COLOR_BGR2GRAY)
  (thresh, im_bw) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  contours, hierarchy = cv2.findContours(im_bw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  print contours

  '''
  for cnt in contours:
    print cnt 
  '''
  #cv2.imshow('img',img)
  cv2.waitKey(0)

def show_co(argv): 
  im = cv2.imread(argv[1], cv2.IMREAD_GRAYSCALE) 
  (thresh, im_bw) = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  detector = cv2.SimpleBlobDetector()
  keypoints = detector.detect(im_bw)
    
  im_with_keypoints = cv2.drawKeypoints(im_bw, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
   
  cv2.imshow("Keypoints", im_with_keypoints)
  cv2.waitKey(0)

if __name__ == "__main__":
  red_image(sys.argv)
