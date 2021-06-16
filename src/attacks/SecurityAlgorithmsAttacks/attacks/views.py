from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .attack.modules.analysis import Analyzer
from .attack.hist_test import *
import skimage 
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
an = Analyzer()

@csrf_exempt
def index(request):
    context = {}
    if request.method == "POST":
        img = request.FILES['uploadFromPC']
        print(img)
        
        if isValidateImage(img.name):
            fs = FileSystemStorage()
            name = fs.save(img.name, img)
            url = fs.url(name)
            context['image_url'] = url
            
            mod_name = protectImage(img)
            mod_name_url = "/media/"+mod_name
            context['hist1'] = "/media/"+"hist_source_"+img.name
            context['hist2'] = "/media/"+"hist1_"+img.name
            context['mod_image_url'] = mod_name_url
            
            an.visual_attack(Image.open(MEDIA_ROOT+"/"+img.name), join=True)
            context['src_lsb_image_url'] = "/media/"+img.name.split(".")[0]+"_LSB.bmp"
            an.visual_attack(Image.open(MEDIA_ROOT+"/"+mod_name), join=True)
            context['mod_lsb_image_url'] = "/media/"+mod_name.split(".")[0]+"_LSB.bmp"
        else:
            messages.warning(request, 'Файл должен иметь разрешение png или jpg!')
            print("VALIDATE ERROR")
        
    return render(request, "attacks/index.html", context)

@csrf_exempt
def comparison(request):
    return render(request, "analysis/comparison_image.html")

