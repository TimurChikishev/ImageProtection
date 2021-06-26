import pandas as pd
from PIL import Image, ImageEnhance
import timeit

def Comparison(Save_Red,Save_Green,Save_Blue,TRed,TGreen,TBlue):
    if set(Save_Red) == set(TRed) and set(Save_Green) == set(TGreen) and set(Save_Blue) == set(TBlue):
        return True
    else:
        return False

def Sharpness(image,factor):
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(factor)
    return image;

def Contrast(image,factor):
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(factor)
    return image;

def Color(image,factor):
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(factor)
    return image;

def Brightness(image,factor):
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(factor)
    return image;

def ColorEmpty(ListColor):
    Color = []
    for i in range(256):
        if i not in ListColor:
            Color.append(i)
    return Color;
    
def RBG(image):
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    Red,Green,Blue = [],[],[]
    for y in range(height):
        for x in range(width):
            p = pix[x, y]
            Red.append(p[0])
            Green.append(p[1])
            Blue.append(p[2])
    return Red,Green,Blue;

def resize_image(original_image,size):
    width, height = original_image.size
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    return resized_image;

def ref(im,Save_Red,Save_Green,Save_Blue):
    TRed,TGreen,TBlue = RBG(im)
    TRed,TGreen,TBlue = ColorEmpty(TRed),ColorEmpty(TGreen),ColorEmpty(TBlue)
    True_False = Comparison(Save_Red,Save_Green,Save_Blue,TRed,TGreen,TBlue)
    return True_False;
    
def main():
    columns=['image_name','transformation','parameters','result_label']
    data = []
    image_list = ['mod_1.png','mod_2.png','mod_3.png','mod_4.png','mod_5.png','mod_6.png','mod_7.png','mod_8.png','mod_9.png','mod_10.png']
    for image in image_list:
        image = Image.open(image)
        Red,Green,Blue = RBG(image)
        Save_Red,Save_Green,Save_Blue = [],[],[]
        print('='*5,image.filename,'='*5)
        Save_Red,Save_Green,Save_Blue = ColorEmpty(Red),ColorEmpty(Green),ColorEmpty(Blue)
        
        im = Sharpness(image,0.9) #Незначительное уменьшение резкости
        data.append([image.filename,"Sharpness",0.9,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Sharpness(image,1.1) #Незначительное повышение резкости
        data.append([image.filename,"Sharpness",1.1,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Contrast(image,0.9) #Незначительное уменьшение контраста
        data.append([image.filename,"Contrast",0.9,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Contrast(image,1.1) #Незначительное повышение контраста
        data.append([image.filename,"Contrast",1.1,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Color(image,0.9) #Незначительное уменьшение цветности
        data.append([image.filename,"Color",0.9,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Color(image,1.1) #Незначительное повышение цветности
        data.append([image.filename,"Color",1.1,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Brightness(image,0.9) #Незначительное уменьшение яркости
        data.append([image.filename,"Brightness",0.9,ref(im,Save_Red,Save_Green,Save_Blue)])
        
        im = Brightness(image,1.1) #Незначительное повышение яркости
        data.append([image.filename,"Brightness",1.1,ref(im,Save_Red,Save_Green,Save_Blue)])

        '''
        im = resize_image(image,size=(800, 600)) #Ресайз до 800*600
        TRed,TGreen,TBlue = RBG(im)
        TRed,TGreen,TBlue = ColorEmpty(TRed),ColorEmpty(TGreen),ColorEmpty(TBlue)
        print("Ресайз до 800*600",TRed,TGreen,TBlue)
        True_False = Comparison(Save_Red,Save_Green,Save_Blue,TRed,TGreen,TBlue)
        data.append([image.filename,"Brightness",1.1,True_False])
        
        im = resize_image(image,size=(1920, 1080)) #Ресайз до 1920*1080
        TRed,TGreen,TBlue = RBG(im)
        TRed,TGreen,TBlue = ColorEmpty(TRed),ColorEmpty(TGreen),ColorEmpty(TBlue)
        print("Ресайз до 1920*1080",TRed,TGreen,TBlue)
        True_False = Comparison(Save_Red,Save_Green,Save_Blue,TRed,TGreen,TBlue)
        data.append([image.filename,"Brightness",1.1,True_False])
        '''
        #print('='*5,image.filename,'='*5)
        #print()
    
    data = pd.DataFrame(data, columns=columns)
    data.to_csv('base.csv')
    print(data)

print(timeit.timeit("main()", setup="from __main__ import main", number=1))   
