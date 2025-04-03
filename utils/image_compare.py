"""
-*- coding: utf-8 -*-
@Time : 4/2/25 
@Author : liuyan
@function : 
"""
from PIL import ImageChops, Image

def compare_images(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    diff = ImageChops.difference(image1, image2)
    return diff.getbbox() is not None
