import cv2
import os
import pytesseract
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
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

def build_and_train_model(data, labels):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(data)

    data = tokenizer.texts_to_sequences(data)
    data = tf.keras.preprocessing.sequence.pad_sequences(data)

    labels = np.array(labels)  

    #LSTM
    model = models.Sequential([
        layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64),
        layers.LSTM(100),
        layers.Dense(len(set(labels)), activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(data, labels, epochs=5)

    return model, tokenizer


image_folder_path = os.path.join(os.path.dirname(__file__), "images")
filenames = os.listdir(image_folder_path)

for filename in filenames:
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(image_folder_path, filename)
        
        detected_text = read_image_and_extract_text(image_path)

        translated_text = translate_to_indonesian(detected_text)
        
        data = [detected_text] * 1000  
        labels = [0] * 1000  
        model, tokenizer = build_and_train_model(data, labels)
    
        input_sequence = tokenizer.texts_to_sequences([detected_text])
        input_sequence = tf.keras.preprocessing.sequence.pad_sequences(input_sequence)
        prediction = model.predict(input_sequence)
        predicted_label = np.argmax(prediction)
   
        translated_label = "Bahasa Inggris" if predicted_label == 0 else "Bahasa Indonesia"

        print("Image:", filename)
        print("Detected Text:", detected_text)
        print("Translated Text:", translated_text)
        print("\n")
