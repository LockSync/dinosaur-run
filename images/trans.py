
# -*- coding: utf-8 -*-
import os
from PIL import Image
 
def transparent_back(filename):
    if(filename.find("png")>=0):
        img = Image.open(filename)
        L, H = img.size
        color_0 = (255,255,255,255)#要替换的颜色
        is_saved=False
        for h in range(H):
            for l in range(L):
                dot = (l,h)
                color_1 = img.getpixel(dot)
                if color_1 == color_0:
                    is_saved=True
                    color_1 = color_1[:-1] + (0,)
                    img.putpixel(dot,color_1)
        if is_saved :
            img.save(filename, "PNG")
            print('done')

transparent_back('blue_cloud.png')
