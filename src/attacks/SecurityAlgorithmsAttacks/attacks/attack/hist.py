import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import cv2 as cv
import seaborn as sns
import inspect
import os
import glob
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

def clear_media(pattern):
    files = glob.glob(MEDIA_ROOT+'/'+pattern)
    for f in files:
        os.remove(f)

# Сверяет два изображения    
def runVisualComparsion(image_1, image_2) -> str:
    rgb_img1 = image_1.copy().convert('RGB')
    rgb_img2 = image_2.copy().convert('RGB')
    result=ImageChops.difference(rgb_img1, rgb_img2)
    new_image = change_brightness(result, 'lighten', 2000)

    clear_media("VisualComparsion*")

    rndsrt = str(uuid.uuid4())
    fname, file_extension = os.path.splitext(image_1.filename)

    fname = "VisualComparsion"+rndsrt+file_extension
    print(fname)
    new_image.save(MEDIA_ROOT+"/"+fname)

    return fname

def change_brightness(image, action, extent):
    pixels = image.getdata()
    new_image = Image.new('RGB', image.size)
    new_image_list = []
    brightness_multiplier = 1.0
    if action == 'lighten':
        brightness_multiplier += (extent/100)
    else:
        brightness_multiplier -= (extent/100)
    for pixel in pixels:
        new_pixel = (int(pixel[0] * brightness_multiplier),
                     int(pixel[1] * brightness_multiplier),
                     int(pixel[2] * brightness_multiplier))
        for pixel in new_pixel:
            if pixel > 255:
                pixel = 255
            elif pixel < 0:
                pixel = 0
        new_image_list.append(new_pixel)
    new_image.putdata(new_image_list)
    return new_image

# Строит гистограммы для каждого канала изображения
def runHistRGB(file_name, num):
    img = cv.imread(file_name)
    color = ("b","g","r")
    
    for i, color in enumerate(color):
        hist = cv.calcHist([img], [i], None, [256], [0, 256])
        plt.xlabel("Bins")
        plt.ylabel("Count")
        plt.plot(hist, color = color)
        plt.xlim([0, 256])
    
    plt.savefig(MEDIA_ROOT+"/"+num+"hist_rgb.png")
    plt.close()
    image = Image.open(file_name)
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
    
    # for Color in [Red,Green,Blue]:
    #     ColorEmpty(Color)
        
    for i,ListColor in enumerate([Red,Green,Blue]):
        if (i == 0):
            color = "Red"
        elif (i == 1):
            color = "Green"
        elif (i == 2):
            color = "Blue"
        plt.xlabel("Bins")
        plt.ylabel("Count")
        sns.histplot(ListColor, bins=256, color = color, element="bars")
        plt.savefig(MEDIA_ROOT+"/"+num+"hist_"+color+".png")
        plt.close()
    

def ColorEmpty(ListColor):
    caller_locals = inspect.currentframe().f_back.f_locals
    for i in range(256):
        if i not in ListColor:
            print(*[name for name, value in caller_locals.items() if ListColor is value],i)
            

