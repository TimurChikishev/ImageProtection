from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .attack.modules.analysis import Analyzer
from .attack.hist_test import *
from .attack.attack import *
from .attack.hist import *
from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import os
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
an = Analyzer()

attacks = [(Attack.VISUAL, "VISUAL"), 
           (Attack.CHI_SQUARE, "CHI_SQUARE"), 
           (Attack.RS, "RS"), 
           (Attack.SPA, "SPA")]

@csrf_exempt
def index(request):
    context = {}
    context["attacks"] = attacks
    try:
        if request.method == "POST":
            data = request.POST
            attack_mod = request.POST['attacs']
            img = request.FILES['uploadFromPC']
            
            if isValidateImage(img.name):
                fs = FileSystemStorage()
                name = fs.save(img.name, img)
                url = fs.url(name)
                context['src_image_url'] = url
                
                mod_name = protectImage(img)
            
                context['hist1'] = "/media/"+"hist_source_"+img.name
                context['hist2'] = "/media/"+"hist1_"+img.name
                context['mod_image_url'] = "/media/"+mod_name
                
                b = case_attack(attack_mod, img.name, mod_name, context)
                if(b == False):
                    messages.warning(request, 'Выберите метод атаки!')
                    
            else:
                messages.warning(request, 'Файл должен иметь разрешение png или jpg!')
            
    except Exception as ex:
        messages.warning(request, str(ex))
        
    return render(request, "attacks/index.html", context)

@csrf_exempt
def comparison(request):
    context = {}
    if request.method == "POST":
        try:
            fs = FileSystemStorage()      
            img = request.FILES 
            img_list = img.getlist('uploadFromPC[]')
            
            if len(img_list) != 2: 
                messages.warning(request, 'Загрузите два файла для сравнения!')
                return render(request, "analysis/comparison_image.html", context)
            
            name1 = fs.save(img_list[0].name, img_list[0])
            name2 = fs.save(img_list[1].name, img_list[1])
            
            img1 = Image.open(MEDIA_ROOT+"/"+img_list[0].name)
            img2 = Image.open(MEDIA_ROOT+"/"+img_list[1].name)
            
            context['first_img'] = fs.url(name1)
            context['second_img'] = fs.url(name2)
            
            structural_similarity(img1, img2, context)
            genAnalisisImage(img1, img2, context)
            
        except Exception as ex:
            messages.warning(request, str(ex))
            
    return render(request, "analysis/comparison_image.html", context)

def case_attack(attack_mod, img_name, img_mod_name, context):
    src_img = Image.open(MEDIA_ROOT+"/"+img_name)
    mod_img = Image.open(MEDIA_ROOT+"/"+img_mod_name)
    
    if(Attack.VISUAL.value == attack_mod):
        an.visual_attack(src_img, join=True)
        an.visual_attack(mod_img, join=True)
        context['src_image_attack_url'] = "/media/"+img_name.split(".")[0]+".bmp"
        context['mod_image_attack_url'] = "/media/"+img_mod_name.split(".")[0]+".bmp"
        
    elif (Attack.CHI_SQUARE.value == attack_mod):
        an.chi_squared_attack(src_img)
        an.chi_squared_attack(mod_img)
        context['src_image_attack_url'] = "/media/"+img_name.split(".")[0]+"_chi.bmp"
        context['mod_image_attack_url'] = "/media/"+img_mod_name.split(".")[0]+"_chi.bmp"
        
    elif (Attack.RS.value == attack_mod):
        src_average = an.rs_attack(src_img)
        mod_average = an.rs_attack(mod_img)
        context['src_average_attack_url'] = (src_average, "Оценка RS на исходном изображении: ")
        context['mod_average_attack_url'] = (mod_average, "Оценка RS на измененном изображении: ")
        
    elif (Attack.SPA.value == attack_mod):
        src_average = an.spa_attack(src_img)
        mod_average = an.spa_attack(mod_img)
        context['src_average_attack_url'] = (src_average, "Оценка SPA на исходном изображении: ")
        context['mod_average_attack_url'] = (mod_average, "Оценка SPA на измененном изображении: ")
        
    else:
        return False
    
    return True

def structural_similarity(img1, img2, context):
    img_a = np.asarray(img1)
    img_b = np.asarray(img2)
    ssimg = ssim(img_a, img_b, multichannel=True) 
    context['ssim'] = ssimg

def genAnalisisImage(img1, img2, context):
    # Визуальное отличие
    runVisualComparsion(img1, img2)
    context['visual_comparsion'] = "/media/"+"visual_comparsion"+os.path.basename(img1.filename)
    
    # RGB hist
    runHistRGB(img1.filename, "1")
    context['img1_hist_rgb'] = "/media/1hist_rgb.png"
    context['img1_hist_red'] = "/media/1hist_Red.png"
    context['img1_hist_green'] = "/media/1hist_Green.png"
    context['img1_hist_blue'] = "/media/1hist_Blue.png"
    
    runHistRGB(img2.filename, "2")
    context['img2_hist_rgb'] = "/media/2hist_rgb.png"
    context['img2_hist_red'] = "/media/2hist_Red.png"
    context['img2_hist_green'] = "/media/2hist_Green.png"
    context['img2_hist_blue'] = "/media/2hist_Blue.png"
    