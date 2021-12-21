import cv2
import pytesseract
import os
import matplotlib.pyplot as plt
import re
import json

def processing():
    img = cv2.imread('img1.png')
    grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2,thresh3 = cv2.threshold(grey_scale,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_data = pytesseract.image_to_string(thresh3, config= '--psm 6')
    final_str = "".join(image_data)
    pattern1 = r'[\%|\*]\s\w*\s?\w*?\s\w+\sNP|[\%|\*]\s\w*\s\w*\s[0-9a-zA-Z]*.[A-Z]+\s\w+|B\w*?\s\w+\sNP|\%\sBEEF\s\w*\s..\/15\sNP'
    pattern2 = r'\d*\.\d+\sF'
    result = re.findall(pattern1, image_data)
    result1 = re.findall(pattern2, image_data)
    result2 = dict(zip(result,result1))
    with open("Bill_Output_n.json", "w") as write_file:
        json.dump(result2, write_file)









processing()

