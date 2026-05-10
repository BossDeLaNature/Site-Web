# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 00:13:05 2025

@author: moito
"""
import pytesseract
import numpy as np
import cv2
from scipy.ndimage import binary_dilation
from scipy.ndimage import generate_binary_structure
from fuzzywuzzy import fuzz


def coordonnee_rectangle(contours_i):
    MAX = contours_i.max(axis=1).max(axis=0)
    MIN = contours_i.max(axis=1).min(axis=0)
    return MIN,MAX
        
        
    


# Reading an image in default mode:
inputImage = cv2.imread("pdf/out16.jpg")
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






# Crop l'image


Min, Max = coordonnee_rectangle(contours[0])

img_crop = inputImage[Min[1]:Max[1],Min[0]:Max[0]]





# Afficher l'image

cv2.namedWindow("yo", cv2.WINDOW_NORMAL)
cv2.imshow("yo",img_crop)
cv2.waitKey(0)


# Identifier le texte



pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

text = pytesseract.image_to_string(img_crop, lang="fra")


def correction_text(text):
    dico = []    #Création d'un dictionnaire pour séparer les différentes phrases du texte
    for i in range(150):
        mot = "Q" + str(i) + ")"
        MOT = "q" + str(i) + ")"
        dico.append(mot)
        dico.append(MOT)
    dico.append("a)")
    dico.append("A)")
    dico.append("b)")
    dico.append("B)")
    dico.append("c)")
    dico.append("C)")
    text = text.replace("Vrai ou Faux", "999")
    text = text.replace("a) Vrai", "12345")
    text = text.replace("b) Faux","45678")
    text = text.replace("\n"," ")
    text = text.replace("Vrai", "")
    text = text.replace("Faux","")
    for i in range(len(dico)):
        text = text.replace(dico[i], "\n")
    text = text.replace("999", "Vrai ou Faux")
    return text


text = correction_text(text)
res = text.split("\n", 10)

print(text)

################################################################################


## Analyser le rouge

hsv = cv2.cvtColor(inputCopy, cv2.COLOR_BGR2HSV)


# Set range for red color 
red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)
    
# define mask
red_mask = cv2.inRange(hsv, red_lower, red_upper)


## Slice the green
imask = red_mask>0
structure = generate_binary_structure(2, 1)
imask_dilated = binary_dilation(imask, structure,15)

red = np.zeros_like(inputCopy, np.uint8)
red1 = 255-red
red1[imask_dilated] = inputCopy[imask_dilated]


black = np.zeros_like(inputCopy, np.uint8)
black1 = 255-black
imask_invert = np.invert(imask_dilated)
black1[imask_invert] = inputCopy[imask_invert]

black_crop = black1[Min[1]:Max[1],Min[0]:Max[0]]


cv2.namedWindow("yo1", cv2.WINDOW_NORMAL)
cv2.imshow("yo1",black_crop)
cv2.waitKey(0)

red_crop = red1[Min[1]:Max[1],Min[0]:Max[0]]

cv2.namedWindow("yo2", cv2.WINDOW_NORMAL)
cv2.imshow("yo2",red_crop)
cv2.waitKey(0)



text_red = pytesseract.image_to_string(red_crop, lang="fra")
text_black = pytesseract.image_to_string(black_crop, lang="fra")


text_red = correction_text(text_red)
res_red = text_red.split("\n", 10)


text_black = correction_text(text_black)
res_black = text_black.split("\n", 10)



## Save 
cv2.imwrite("red.png", red1)
cv2.imwrite("black.png", black1)






######################### CREATION JEUX DE DONNEES


import pandas as pd



infoBat = pd.DataFrame({'Question' : ["Paris"], \
                        'Proposition' : ["Paris"], \
                        'Reponse' : [True]}, \
                        columns = ["Question","Proposition","Reponse"])
infoBat

def ajout_info(res, res_black, res_red):
    data_vide = pd.DataFrame({'Question' : ["Paris","Paris","Paris"], \
                            'Proposition' : ["Paris","Paris","Paris"], \
                            'Reponse' : [False, False, False]}, \
                            columns = ["Question","Proposition","Reponse"])
    data_vide.at[0, "Question"] = res[0]
    data_vide.at[1, "Question"] = res[0]
    data_vide.at[2, "Question"] = res[0]
    data_vide.at[0, "Proposition"] = res[1]
    data_vide.at[1, "Proposition"] = res[2]
    data_vide.at[3, "Proposition"] = res[2]
    for i in range(3):
        for j in range(len(res_black)):
            if len(res_black[j])>10:
                similarite = fuzz.partial_ratio(res[i+1].lower(), res_black[j].lower())
                if similarite > 90:
                    data_vide.at[i, "Reponse"] = True
                    text = res_black[j]
                    text = text.replace(" ","")
                    if text.endswith("12345"):
                        data_vide.at[i, "Reponse"] = False
    data_vide.drop(data_vide.index[-1], inplace=True)
    return data_vide


data_vide = ajout_info(res, res_black, res_red)




