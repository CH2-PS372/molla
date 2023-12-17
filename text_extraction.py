import cv2
import os
import pytesseract
import numpy as np
import tensorflow as tf
from keras import layers, models
from googletrans import Translator


# Fungsi untuk membersihkan dan memproses teks
def preprocess_text(text):
    cleaned_text = text.lower()  # Menyederhanakan dengan mengonversi ke huruf kecil
    return cleaned_text


# Fungsi untuk membaca gambar dan ekstraksi teks
def read_image_and_extract_text(image_path):
    print("Reading image:", image_path)

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found - {image_path}")
        return

    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Error: Unable to read the image - {image_path}")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray_image)
    cleaned_text = preprocess_text(text)
    print("Extracted text:", cleaned_text)
    return cleaned_text


def translate_to_indonesian(text):
    if text is None:
        print("Error: Text is None. Cannot translate.")
        return None

    translator = Translator()
    translated_text = translator.translate(text, dest='id').text
    return translated_text


# Fungsi untuk membangun dan melatih model
def build_and_train_model(data, labels, num_classes):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(data)

    data = tokenizer.texts_to_sequences(data)
    data = tf.keras.preprocessing.sequence.pad_sequences(data)

    labels = np.array(labels)

    # LSTM
    model = models.Sequential([
        layers.Embedding(input_dim=len(tokenizer.word_index) + 1, output_dim=64),
        layers.LSTM(100),
        layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(data, labels, epochs=5)

    return model, tokenizer


# Lokasi direktori dataset
dataset_folder = os.path.join(os.path.dirname(__file__), "images")

# Daftar nama file dalam direktori dataset
filenames = os.listdir(dataset_folder)

# Data dan label untuk pelatihan model
data = []
labels = []

for filename in filenames:
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(dataset_folder, filename)

        detected_text = read_image_and_extract_text(image_path)

        # Tambahkan teks yang telah diproses dan label ke dalam data pelatihan
        data.append(detected_text)
        labels.append(0)

    # Jumlah kelas
num_classes = 2

# Membangun dan melatih model
model, tokenizer = build_and_train_model(data, labels, num_classes)

# Contoh pemindaian gambar dan terjemahan
example_image_path = r'D:\Dewi\Api_mola\images\sample11.png'
example_image_path_full = os.path.join(os.getcwd(), example_image_path)
detected_text = read_image_and_extract_text(example_image_path_full)

# Terjemahkan teks yang dihasilkan dari pemindaian
translated_text = translate_to_indonesian(detected_text)

# Tampilkan hasil pemindaian dan terjemahan
print("Detected Text:", detected_text)
print("Translated Text:", translated_text)

# Input sequence dan prediksi menggunakan model
input_sequence = tokenizer.texts_to_sequences([detected_text])
input_sequence = tf.keras.preprocessing.sequence.pad_sequences(input_sequence)
prediction = model.predict(input_sequence)
predicted_label = np.argmax(prediction)
translated_label = "Bahasa Inggris" if predicted_label == 0 else "Bahasa Indonesia"

model.save(r'model.h5')


