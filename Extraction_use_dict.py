import cv2 as cv
import pytesseract
from typing import OrderedDict
import re
from glob import glob

# def loading(a):
#     lis = []
#     file = glob(a)
#     for i in file:
#         reading = cv.imread(i)
#         lis.append(reading)
#     return lis
# lis = loading('/home/sharbadeepa/testing invoice today/*.jpeg')
# print("==========",lis[1])


img = cv.imread('invoice.jpg')

image_str = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

data_dict = OrderedDict({
    'Invoice':{'label': '#','zoning_type':'bottom_large'},
    'Bill_No':{'label': 'Bill','zoning_type':'Inline'},
    'Shipping':{'label': 'Shipping','zoning_type':'Inline'},
    'Invoice_Date':{'label': 'Date','zoning_type':'Inline'},
})

final_op = {
    'Invoice':"",
    'Bill_No':"",
    'Shipping':"",
    'Invoice_Date':"",
}

for key in data_dict.keys():
    to_find =data_dict[key]['label'].lower()
    for i in range(len(image_str['text'])):
        if to_find in image_str['text'][i].lower():
            x,y,w,h = image_str['left'][i], image_str['top'][i], image_str['width'][i], image_str['height'][i]
            if data_dict[key]['zoning_type'] == 'bottom_large': 
                zoning_type = (x-10,y-20,w+x+230,h+y+10)  
            else:
                zoning_type = (x-10,y-20,w+x+290,h+y+80)  
            break
    
    for i in range(len(image_str['text'])):
        x,y,w,h = image_str['left'][i], image_str['top'][i], image_str['width'][i], image_str['height'][i]
        if x>=zoning_type[0] and y>=zoning_type[1] and w+x<=zoning_type[2] and h+y<=zoning_type[3]:
            final_op[key] += image_str['text'][i]+""

for key,val in final_op.items():
    final_op[key] = re.sub(r'\s+', r'',(re.sub('Invoice #:|BILL TO:|SHIPPING TO:|Invoice Date','', val)).strip())

    # final_op[key] = re.sub(r'\s+',r' ', (re.sub('BILL TO:|#|Due:|Grand Total','', val)).strip())

print(final_op)
