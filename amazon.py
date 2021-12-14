import cv2 as cv
import pytesseract
from typing import OrderedDict

import re
import json
from math import ceil



from pytesseract.pytesseract import image_to_data

img = cv.imread('amazon_invoice.png')
image_data = pytesseract.image_to_data(img,  output_type=pytesseract.Output.DICT)
print(image_data['text'])

# regex_date = re.findall(r'O\w+\s\w+\:\s\d{1,2}\.\d{1,2}\.\d{2,4}', image_data)
# regex_pan = re.findall(r'P\w+\s\w+\:\s\w*', image_data)
# regex_billing = re.findall(r'J\w+\s\w*\n\d+\,[\s\w+\s\w\,]+', image_data)
# regex_Gst = re.findall(r'G\w+\s\w*\s\w*\:\s\|\w*', image_data)
# regex_item = re.findall(r'H\w+\s\w+\s\w+\s\w+\s\w+', image_data)
# regex_unit = re.findall(r'\§\d+\.\d+', image_data)
# regex_total = re.findall(r'\$\d{2}\.\d+', image_data)


# result = ('Date : {}, PAN : {}, Billing: {}, GST: {}, Item : {}, Unit : {}, TOtal:{}'.
# format(regex_date,regex_pan,regex_billing,regex_Gst,regex_item,regex_unit,regex_total))
# stud_obj = json.dumps(result)
# print((stud_obj))




data_dict = OrderedDict({
    'PAN':{'label': 'PAN','Pattern':'[A-Z]{3}\d{6}[A-Z]','zoning_type':'in_line'},
    'Billing':{'label': 'Billing','Pattern':'(.*)Shipping\s?Address','zoning_type':'left_bottom_large'},
    'Order_date':{'label': 'Date','Pattern':'\d{1,2}[\.-//]\d{1,2}[\.-//]\d{2,4}', 'zoning_type':'in_line'},
    'Gst':{'label': 'GST','Pattern':'\.?[A-Za-z]{1,2}\d{7}[A-Za-z]{2}','zoning_type':'in_line'},
    'Invoice Number':{'label': 'Invoice','Pattern':'[A-Za-z]{3}\d{6}','zoning_type':'in_line'},
    'Item':{'label': 'Description','Pattern':'(\w*)(Unit\s?Price|\$)','zoning_type':'left_bottom_right_large'},
    'Unit ':{'label': 'Unit', 'Pattern':'\$\d+\.?\d+', 'zoning_type':'bottom_large'},
    'Total':{'label':'Total', 'Pattern':'\$?\d{1,4}?\.?\d{1,4}?(\$\d+\.?\d+)','zoning_type':'in_line'}
})



final_op = {
    'Pan':"",
    'Billing':"",
    'Order_date':"",
    'Gst':"",
    'Invoice Number'
    'Item':"",
    'Unit':"",
    'Total':"",
}



for key in data_dict.keys():
    to_find = data_dict[key]['label'].lower()
    for i in range(len(image_data['text'])):

        if to_find in image_data['text'][i].lower():
            x,y,w,h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]
            
            if data_dict[key]['zoning_type'] == "in_line":
                zoning_area = (x-10,y-10,w+x+430,h+y+10) 
            elif data_dict[key]['zoning_type'] == "left_bottom_right":
                zoning_area = (x-190,y-10,w+x+10,h+y+200) 
            elif data_dict[key]['zoning_type'] == "bottom_large":
                zoning_area = (x-w,y-10,w+x+w,h+y+50) 
            else:
                zoning_area = (x-150,y+20,w+x+430,h+y+100)

            temp_Str=""
            # if final_op[key] == "":
            for j in range(len(image_data['text'])):
                    x,y,w,h = image_data['left'][j], image_data['top'][j], image_data['width'][j], image_data['height'][j]
                    
                    if x>=zoning_area[0] and y>=zoning_area[1] and x+w <= zoning_area[2] and y+h <= zoning_area[3]:
                        temp_Str += image_data['text'][j]+' '
                
            if re.findall(data_dict[key]['Pattern'], temp_Str):
                final_op[key] = re.findall(data_dict[key]['Pattern'], temp_Str)[0]
                print(final_op[key])

         
f = open(f"{final_op['Invoice Number']}.json", 'w')
final_op = {key:final_op[key] for key in final_op.keys()}
json.dump(final_op, f)


# f.close()



    

          

