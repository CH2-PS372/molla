import cv2
import os
import pytesseract
import numpy as np
from googletrans import Translator

#membaca gambar dan ekstraksi teks
def read_image_and_extract_text(image_path):
    print("Reading image:", image_path)
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    print("Extracted text:", text)
    return text

#menerjemahkan teks dari bahasa Inggris ke bahasa Indonesia
def translate_to_indonesian(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='id').text
    return translated_text