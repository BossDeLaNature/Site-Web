# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 00:13:05 2025

@author: moito
"""

from PIL import Image, ImageChops
import pytesseract

import numpy as np
import cv2
import re


def coordonnee_rectangle(contours_i):
    MAX = contours_i.max(axis=1).max(axis=0)
    MIN = contours_i.max(axis=1).min(axis=0)
    return MIN,MAX
        
        
    


# Reading an image in default mode:
inputImage = cv2.imread("pdf/out1.jpg")
inputCopy = inputImage.copy()

# The HSV mask values:
lowerValues = np.array([58, 151, 25])
upperValues = np.array([86, 255, 75])

# Creating kernel 
kernel = np.ones((1,80), np.uint8) 
kernel2 = np.ones((80, 1), np.uint8) 

kernel3 = np.ones((100, 100), np.uint8) 

kernel4 = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))

# Convert the image to HSV:
gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

inverse = 255-gray

ret,thresh = cv2.threshold(inverse,127,255,cv2.THRESH_BINARY)
horizontal = cv2.erode(thresh, kernel)
horizontal2 = cv2.dilate(horizontal,kernel)
vertical = cv2.erode(thresh, kernel2)
vertical2 = cv2.dilate(vertical, kernel2)
carre = horizontal2 + vertical2
carre2 = cv2.morphologyEx(carre,cv2.MORPH_OPEN,kernel4)

carre3 = cv2.morphologyEx(carre2,cv2.MORPH_OPEN,kernel4)

ret,thresh5 = cv2.threshold(inverse,127,255,cv2.THRESH_BINARY)
# Create the HSV mask
# mask = cv2.inRange(noise2, 0, 254)

Dezoom = cv2.resize(thresh, (708, 1002)) 


contours, hierarchy = cv2.findContours(carre3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

im = cv2.drawContours(inputImage, contours, 0, (0,255,0), 3)


Min, Max = coordonnee_rectangle(contours[4])

img_crop = inputImage[Min[1]:Max[1],Min[0]:Max[0]]

cv2.namedWindow("yo", cv2.WINDOW_NORMAL)
cv2.imshow("yo",img_crop)
cv2.waitKey(0)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

text = pytesseract.image_to_string(img_crop, lang="fra")
text = text.replace("\nb)","123456")
text = text.replace("\nc)","123456")
text = text.replace("\na)","123456")
text = text.replace("\nB)","123456")
text = text.replace("\nC)","123456")
text = text.replace("\nA)","123456")
text = text.replace("\n"," ")
text = text.replace("123456","\n")
text = text.replace("PaO»","PaO2")
text = text.replace("b) c) Vai CJ | Faux LJ a C)","")
text = text.replace("a) ","")
text = text.replace("b}","")
text = text.replace("C)","")
text = text.replace("Vrai","")
text = text.replace("Faux","")
text = text.replace("C)","")
text = text.replace("C)","")
res = text.split("\n", 5)

print(text)