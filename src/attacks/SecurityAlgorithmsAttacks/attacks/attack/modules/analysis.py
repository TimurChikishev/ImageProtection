from PIL import Image
from PIL.ExifTags import TAGS
import os
import logging
from ..methods.chi_square import chi_squared_test
from ..methods.sample_pairs import spa_test
from ..methods.rs import rs_test
import numpy as np
from pathlib import Path

class Analyzer:
    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = os.path.join(BASE_DIR, 'static\\media')
    
    def __init__(self, log_lvl=logging.INFO):
        pass
        # logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s', level=log_lvl)

    def visual_attack(self, img, join=False, bitnum=1):
        """Implementing a visual attack

        Visual attack can be of two kinds.
        In the first case, three images of channels with LSB 
        are created, in the second, these three images are 
        combined into one. Images are opened by means of 
        the operating system.

        :param img: Image for attack
        :param join: Is it necessary to divide the image into channels
        :param bitnum: How many LSBs need to take

        """
        bitnum = int(bitnum)
        # logging.info('Visualising lsb for '+ img.filename +' ...🌀')
        height, width = img.size
        if join == False:
            channels = img.split()
            colors = [(0, 0, 0), (0, 255, 0), (0, 0, 255)] # red, green, blue
            suffixes = ['red', 'green', 'blue']

            for k in range(3):
                channel = channels[k].load()
                img_ch = Image.new("RGB", (height, width), color=colors[k])

                for i in range(height):
                    for j in range(width):
                        bit = int((bin(channel[i, j]))[-bitnum]) # takes LSB
                        if bit == 1:
                            if k == 0:
                                img_ch.putpixel((i, j), 255) # black
                            else:
                                img_ch.putpixel((i, j), 0) # white
                name = suffixes[k] + "-" + img.filename.split(".")[0] + ".bmp"
                img_ch.save(name)
                # logging.info("Openning " + suffixes[k] + " component...🌀")
                # img_ch.show()
        else:
            img_ch = Image.new("RGB", (height, width), color=(0, 0, 0))
            for i in range(height):
                for j in range(width):
                    pixel = img.getpixel((i, j))
                    if len(pixel) == 4: # if RGBA
                        pixel = pixel[:-1]
                    new_pixel = [0, 0, 0]
                    for k in range(3):
                        if int(bin(pixel[k])[-1]) == 1:
                            new_pixel[k] = 255
                        else:
                            new_pixel[k] = 0

                    img_ch.putpixel((i, j), tuple(new_pixel))
                    
            # print(self.MEDIA_ROOT)
            # print("-------")
            # print(img.filename.split(".")[0])
            # print("+++")
            # print(img.filename.split(".")[0] + "_LSB.bmp")
            img_ch.save(img.filename.split(".")[0] + ".bmp")
            # logging.info("Openning LSB image...🌀")
            # img_ch.show()

    def chi_squared_attack(self, img, eps=1e-5):
        """Implementing a chi-squared attack

        Westfeld and Pfitzmann attack using chi-square test.
        The paper describing this method can be found here:
        http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.94.5975&rep=rep1&type=pdf 
        The test is applied to each line, then the original image 
        is colored in accordance with the result. 
        A new image with a test result is saved in the current directory.


        :param img: Image for attack
        :param eps: Error value for probability  (default is 1e-5)
        
        """
        #  logging.info('Calculating chi_squared for '+ img.filename +' ...🌀')
        channels = img.split()
        width, height = img.size

        img_to_blend = Image.new(img.mode, (width, height), color=(0, 0, 0)) # image with results 
    
        for i in range(height):
            prob = 0
            for ch in channels:
                data = ch.crop((0, i, width, i+1)) # crop for new line 
                prob += chi_squared_test(data)[1]
            prob /= 3
            if 0.5 - eps < prob < 0.5 + eps: 
                for j in range(width):
                    img_to_blend.putpixel((j, i), (209, 167, 27)) # yellow
            elif prob < 0.5 - eps:
                for j in range(width):
                    img_to_blend.putpixel((j, i), (112, 209, 27)) # green
            elif prob > 0.5 + eps:
                for j in range(width):
                    img_to_blend.putpixel((j, i), (255, 0, 0)) # red

        result = Image.blend(img, img_to_blend, 0.5)
        result.save(img.filename.split(".")[0] + "_chi.bmp")
        
        # result.show()

    def spa_attack(self, img):
        # logging.info("Calculating spa beta for " + img.filename +' ...')
        estimate = spa_test(img)
        return estimate
        # logging.info("SPA estimate for "+ img.filename + " is " + str(estimate))

    def rs_attack(self, img):
        # logging.info("Calculating rs estimate for " + img.filename +' ...🌀')
        # logging.info("It will take a couple of minutes...")
        estimate = rs_test(img)
        return estimate
        # logging.info("RS estimate for "+ img.filename + " is " + str(estimate))

if __name__ == "__main__":
    an = Analyzer()
    an.visual_attack(Image.open("30.png"))
    # an.attack_chi_squared(mode="real")

