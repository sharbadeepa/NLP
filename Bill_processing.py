import cv2
from nltk.translate.ribes_score import kendall_tau
import pytesseract
import os
import matplotlib.pyplot as plt
import re
import json
import nltk
from typing import OrderedDict
from fuzzywuzzy import fuzz

label =  OrderedDict({'item1':'365 BACON LS', 'item2':'FLOUR ALMOND', 
'item3':'CHICKEN BREAST BNLSS SK', 'item4':'HEAVY CREAM', 'item5':'BALSHC aepuct', 
'item6':'BEEF GROUND', 'item7':'JUICE or CASHEW', 'item8':'POCS PINT ARGANIC', 'item9':'HONEY ALMOND BUTTER'})

def processing():
    img = cv2.imread('img1.png')
    grey_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret2,thresh3 = cv2.threshold(grey_scale,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_data = pytesseract.image_to_string(thresh3, config= '--psm 6')
    final_str = "".join(image_data)
    lis = []

    for i in label.values():
        a = i.split(' ')
        ngram_len = len(a)
        ngram = nltk.ngrams(image_data.split(' '), ngram_len)
        for j in ngram:

            if fuzz.ratio(i, j) > 60:
                print(i)
                j = i
                lis.append(j)
    pattern = r'\d*\.\d+\sF'
   
    result1 = re.findall(pattern, image_data)
    result2 = dict(zip(lis,result1))
    # print(result2)
    with open("Bill_Output_new.json", "w") as write_file:
        json.dump(result2, write_file)


                
               




processing()


   



        
        

      


