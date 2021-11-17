from django.shortcuts import render
from django.conf import settings

import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract


def index(request):
    context = {"full_filename" : 'images/white_bg.jpg'}

    if request.method == "POST":
        image_upload = request.FILES['image_upload']
        image = Image.open(image_upload.file)

        # Converting image to array
        image_arr = np.array(image.convert('RGB'))
		# Converting image to grayscale
        gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
		#Converting image back to rbg
        image = Image.fromarray(gray_img_arr)

		# Printing lowercase
        letters = string.ascii_lowercase
		# Generating unique image name for dynamic image display
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename =  'uploads/' + name

		# Extracting text from image
        custom_config = r'-l eng --oem 3 --psm 6'
        pytesseract.pytesseract.tesseract_cmd = './.apt/usr/bin/tesseract'
        text = pytesseract.image_to_string(image,config=custom_config)

		# Remove symbol if any
        characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
        new_string = text
        for character in characters_to_remove:
            new_string = new_string.replace(character, "")

		# Converting string into list to dislay extracted text in seperate line
        new_string = new_string.split("\n")

		# Saving image to display in html
        img = Image.fromarray(image_arr, 'RGB')
        img.save(settings.BASE_DIR / f"static/uploads/{name}")
        context = {"full_filename": full_filename, "text": new_string}

    return render(request, "index.html", context)