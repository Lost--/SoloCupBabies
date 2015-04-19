#!/usr/bin/python

import cv2 
import numpy as np
import sys

def main (argv):
  img = cv2.imread(argv[1])
  lower = np.array([10, 10, 150], dtype ="uint8")
  upper = np.array([60, 60, 250], dtype="uint8")
  mask = cv2.inRange(img, lower, upper)
  output = cv2.bitwise_and(img, img, mask=mask)
  outgray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
  ret,thresh = cv2.threshold(outgray,127,255,0)
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  print contours
  for cnt in contours:
    print cnt

  '''
  contours, hier = cv2.findContours(output,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  for cnt in contours:
    if 200<cv2.contourArea(cnt)<5000:
      cv2.drawContours(img,[cnt],0,(0,255,0),2)
      cv2.drawContours(mask,[cnt],0,255,-1)

  cv2.waitKey(0)
  '''
if __name__ == "__main__":
  main(sys.argv)
