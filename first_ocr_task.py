
import cv2 as cv
import pytesseract

img = cv.imread('invoice-practice1.png')
image_str = pytesseract.image_to_data(img, output_type = pytesseract.Output.DICT)


key_vals = ['TO:', "#", "Date", "Total"]
for i in key_vals:
    to_find = i
    new = ""
    for j in range(len(image_str['text'])):

        if to_find in image_str['text'][j]:

            x,y,w,h = image_str['left'][j],image_str['top'][j], image_str['width'][j],image_str['height'][j]
            if to_find ==  'TO:':
                print("iffff")
                zoning_area = (x-300,y-600,x+w+90,h+y+200)
            else:
                zoning_area = (x-100,y-10,x+w+900,h+y+100)
            break    

    for i in range(len(image_str['text'])):
        x,y,w,h = image_str['left'][i],image_str['top'][i], image_str['width'][i],image_str['height'][i]
        if x>=zoning_area[0] and y>=zoning_area[1] and x+w<=zoning_area[2] and h+y<=zoning_area[3]:
            new += image_str['text'][i]+" "
    print(f"{to_find} = {new}")



        


