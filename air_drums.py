# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 22:35:07 2022

@author: nilay
"""

import cv2
import numpy as np
import time
import pygame
from pygame import mixer

mixer.init()

vid = cv2.VideoCapture(0)
radius = [0,0,0,0,0,0]

class The:
    def __init__(self):
        self.i = 1
    
index_manager = The()


def radius_check(radius):
    if radius[index_manager.i+5] > radius[index_manager.i]:
        #print("Increasing")
        return True
    elif radius[index_manager.i+5] < radius[index_manager.i]:
        #print("Decreasing")
        return False
    else:
        #print("Constant")
        return False
    
    


prev_frame_time = 0
prev = 0
new_frame_time = 0
func_time = 0
j = -10

while(True):
    ret, img = vid.read(0)
    #img = cv2.resize(img,(320,240),fx=0,fy=0,interpolation= cv2.INTER_CUBIC)
    img  = cv2.flip(img,1) 
    cv2.rectangle(img,(50,100),(250,250),(0,0,255),2)
    cv2.rectangle(img,(400,100),(600,250),(0,0,255),2)
    cv2.rectangle(img,(25,300),(175,450),(0,0,255),2)
    cv2.rectangle(img,(225,300),(375,450),(0,0,255),2)
    cv2.rectangle(img,(425,300),(575,450),(0,0,255),2)
    
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = str(int(fps))
    cv2.putText(img, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)

    gray_blurred = cv2.blur(gray, (3, 3))

    detected_circles = cv2.HoughCircles(gray_blurred, 
                       cv2.HOUGH_GRADIENT, 1, 20, param1 = 50,
                       param2 = 35  , minRadius = 1, maxRadius = 70)
    min=[255,255,255];
    max=[0,0,0];
    if detected_circles is not None:
        
        detected_circles = np.uint16(np.around(detected_circles))
        if j==0:
            j = -1
        if j==1:
            j = -2
        if j==2:
            j = -3
        if j==3:
            j = -4
        if j==4:
            j = -5

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            cv2.circle(img, (a, b), r, (0, 255, 0), 2)

            cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
            #print(r) 
            radius.append(r)
            print(len(radius))
            #Conditions to check box boundaries (5 for 5 drums)
            if a > 50 and a < 250 and b > 100 and b < 250 and r > 25 and r < 37 :
                if radius_check(radius) and j != -1:
                    cv2.circle(img, (a, b), r, (0, 0, 255), 2)
                    drum1 = mixer.Sound('path')
                    drum1.play()
                    j = 0
                    break
            elif a>400 and a<600 and b>100 and b<250 and r>25 and r>37 :
                if radius_check(radius) and j != -2:
                    cv2.circle(img, (a, b), r, (0, 0, 255), 2)
                    drum2 = mixer.Sound('path')
                    drum2.play()
                    j = 1
                    break
            if a>25 and a<175  and b>300 and b<450 and r>25 and r<37:
                if radius_check(radius) and j!=-3:
                    cv2.circle(img, (a, b), r, (0, 0, 255), 2)
                    drum3 = mixer.Sound('path')
                    drum3.play()
                    j = 2
                    break
            if a>225 and a<375 and b>300 and b<450 and r>25 and r<37:
                if radius_check(radius) and j!=-4:
                    cv2.circle(img, (a, b), r, (0, 0, 255), 2)
                    drum4 = mixer.Sound('path')
                    drum4.play()
                    j = 3
                    break
            if a> 425 and a<575 and b>300 and b<450 and r>25 and r>37:
                if radius_check(radius) and j!= -5:
                    cv2.circle(img, (a, b), r, (0, 0, 255), 2)
                    drum5 = mixer.Sound('path')
                    drum5.play()
                    j = 4
                    break


    cv2.imshow("Detected Circle", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()