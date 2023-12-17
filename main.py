from flask import Flask, request, jsonify
import cv2
import os
import pytesseract
import numpy as np
import tensorflow as tf
from keras import layers, models
from googletrans import Translator

app = Flask(__name__)

# Load the pre-trained model and tokenizer
model = tf.keras.models.load_model(r'D:\Dewi\Api_mola\model.h5')
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.word_index = {'': 0}

# Fungsi untuk membersihkan dan memproses teks
def preprocess_text(text):
    text_resize = text.lower()  # Menyederhanakan dengan mengonversi ke huruf kecil
    cleaned_text = text_resize.replace("\n", " ")

    return cleaned_text

# Fungsi untuk membaca gambar dan ekstraksi teks
def read_image_and_extract_text(image_path):
    print("Reading image:", image_path)
    # Check if the file exists
    if not os.path.exists(image_path):
        return jsonify({"error": f"File not found - {image_path}"}), 400

    image = cv2.imread(image_path)
    # Check if the image is loaded successfully
    if image is None:
        return jsonify({"error": f"Unable to read the image - {image_path}"}), 400

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    cleaned_text = preprocess_text(text)
    return jsonify({"extracted_text": cleaned_text})

# Fungsi untuk terjemahan
def translate_to_indonesian(text):
    if text is None:
        return jsonify({"error": "Text is None. Cannot translate."}), 400

    translator = Translator()
    translated_text = translator.translate(text, dest='id').text
    return jsonify({"translated_text": translated_text})

# Endpoint untuk membaca gambar dan ekstraksi teks
@app.route('/read_image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_path = os.path.join(app.config['uploads'], image_file.filename)
    image_file.save(image_path)

    return read_image_and_extract_text(image_path)

# Endpoint untuk terjemahan
@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    if 'text' not in data:
        return jsonify({"error": "No text provided for translation"}), 400

    text = data['text']
    return translate_to_indonesian(text)

if __name__ == '__main__':
    app.config['uploads'] = r'uploads'
    app.run(debug=True)
