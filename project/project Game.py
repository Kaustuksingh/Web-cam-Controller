# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 00:15:26 2021

@author: VIVEK SINGH
"""

import cv2
import pyautogui
import numpy as np

def max_cnt(contours) :
    cnt = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(contours[i])
        if(area > max_area):
            cnt = i
            max_area = area
    return cnt


vid = cv2.VideoCapture(0)
prev_pos= "neutral"

while (1):
    _,frame = vid.read()
    frame=cv2.flip(frame,1)
    frame =frame[0:300,300:600]
    frame= cv2.GaussianBlur(frame,(5,5),2)
    lower = np.array([13,16,28])
    upper = np.array([87,93,125])
    mask = cv2.inRange(frame,lower,upper)
    contours,heirarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cont = cv2.drawContours(frame,contours,-1,(0,0,255),3)
    
    if len(contours) == 0:
        continue
    
    max_contour = max(contours,key = cv2.contourArea)

    epsilon = 0.01*cv2.arcLength(max_contour,True)
    max_contour = cv2.approxPolyDP(max_contour,epsilon,True)
    
    
    M = cv2.moments(max_contour)
    try:
        x= int(M['m10']/M['m00'])
        y= int(M['m01']/M['m00'])
    except ZeroDivisionError:
        continue
    frame = cv2.circle(frame,(x,y),5,(255,0,0),3)
    frame = cv2.drawContours(frame, [max_contour], -1, (0,0,255), 3)
    frame = cv2.line(frame,(75,0),(75,299),(255,255,255),3)
    frame = cv2.line(frame,(225,0),(225,299),(255,255,255),3)
    frame = cv2.line(frame,(0,175),(299,175),(255,255,255),3)
    frame = cv2.line(frame,(0,250),(299,250),(255,255,255),3)
    
    cv2.imshow('DIP',frame)
    
    if x < 75:
        curr_pos = "left"
    elif x >225 :
        curr_pos="right"
    elif y < 175 and x > 75 and x < 225 :
        curr_pos = "up"
    elif y >250 and x > 75 and x < 225 :
        curr_pos= "down"
    else:
        curr_pos= "neutral"
        
    if curr_pos != prev_pos:
        if curr_pos != "neutral":
            pyautogui.press(curr_pos)
        prev_pos = curr_pos
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()