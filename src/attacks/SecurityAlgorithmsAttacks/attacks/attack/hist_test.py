import imageio
import matplotlib.pyplot as plt
import numpy as np
import random
from PIL import Image
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')

def isValidateImage(img) -> bool:
    print("img: ", img)
    if img.endswith('.png') or img.endswith('.jpg'):
        return True
    else:
        return False
    
def protectImage(img):
    file_name = img.name
    print(MEDIA_ROOT+"/"+file_name)
    img = imageio.imread(MEDIA_ROOT+"/"+file_name)
    print(img)
   
    gray = rgb2gray(img)
    print(gray)
    gray = gray.astype(np.int64)
    print(gray)
    
    plt.hist(gray.flatten(), bins=256, facecolor='black', alpha=1)
    plt.grid('off') 
    plt.axis('off')
    plt.title('Histogram of the source image')
    plt.savefig(MEDIA_ROOT+"/"+"hist_source_"+file_name)
    plt.close()
    
    H = plt.hist(gray.flatten(), bins=256, facecolor='black', alpha=1)
    int_values = getmask(H[0], 4) # just modify the percent of the pixel values taken
    print("returned values for this image") 
    print(int_values)
    
    array_lum_val = []
    n, bins, patches = plt.hist(gray.flatten(), bins=256, align='left', color='black')
    for values in int_values:
        for i in values:
            patches[i].set_fc('r')
            array_lum_val.append(i)

    plt.grid('off') 
    plt.axis('off')
    plt.title('Resulting histogram (black) with selected regions (red)')
    plt.savefig(MEDIA_ROOT+"/"+"hist1_"+file_name)
    plt.close()
    
    array_lum_val.sort()    
    print(array_lum_val) # luminance values selected
    
    for i in array_lum_val:
        img[img==i] = i+1

    # plt.hist(gray.flatten(), bins=256, facecolor='black', alpha=1)
    # plt.grid('off') 
    # plt.axis('off')
    # plt.savefig(MEDIA_ROOT+"/"+"hist2_"+file_name)
    
    imageio.imwrite(MEDIA_ROOT+"/"+"mod_"+file_name, img)
    
    return "mod_"+file_name

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114]) # luminance channel

#Image sub-part selection
#The method to extract a sub-part of the image is based on the image intensity histogram.
#We select image regions using the following scheme: The user defins the approximate desired percent of the image to be extracted (i.e, a percent of all the image pixels).
#Then a sub-part with width of 9 bins is randomly selected and exctracted from the histogram.
#The process in repeated untill the number of pixels from the original grayscale image selected is equal (or bigger) than the percent specified by the user.
#The proposed algorithms works for natural images, where the histogram has values in all the spectra, which are evenly distributed.
def getmask(imhist,percent=10):
    ''' function takes the histogram and % of the pixels for the mask, and takes the  approx% of the values from the right part of hist.
    The returned value is the pixel intensity value which will be used as a threshold later'''
    taken_pix = 0
    total_pix = np.sum(imhist, axis = 0)
    indexes_to_return = []
    while taken_pix<=percent:
        rand_hist_val = random.randint(4, 128) # take a random initialization  
        random_hist_part = np.sum(imhist[rand_hist_val-1:rand_hist_val+1],axis=0)
        imhist[rand_hist_val-1:rand_hist_val+1] = 0 # we put zeros to the values already taken
        indexes_to_return.append(range(rand_hist_val-1,rand_hist_val+1))
        taken_pix += (random_hist_part/total_pix)*100
        
    
    return indexes_to_return # attention! works with natural images only with colors in different parts of hist.