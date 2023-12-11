import pandas as pd
import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from flask import Flask, request, jsonify

tf.keras.mixed_precision.set_global_policy('float32')

dataset_path = 'dataUji.tsv'
df = pd.read_csv(dataset_path, sep='\t', header=None, names=['num_eng', 'sent_eng', 'num_indo', 'sent_indo'])

model_path = '/home/destucr/molla/tflite/model.tflite'
interpreter = tf.lite.Interpreter(model_path = model_path)
interpreter.allocate_tensors()

tokenizer_eng = Tokenizer()
tokenizer_eng.fit_on_texts(df['sent_eng'])
max_len_eng = 72
tokenizer_indo = Tokenizer()
tokenizer_indo.fit_on_texts(df['sent_indo'])
max_len_indo = max([len(seq) for seq in tokenizer_indo.texts_to_sequences(df['sent_indo'])])

def create_shuffled_sentence(sentence):
    words = sentence.split()
    random.shuffle(words)
    return ' '.join(words)

def evaluate_user_input(user_input, original_sentence):
    user_input_lower = user_input.lower()
    original_sentence_lower = original_sentence.lower()

    if user_input_lower == original_sentence_lower:
        print("Jawaban benar!")
        return True
    else:
        print(f"Jawaban salah. Jawaban yang benar adalah:\n{original_sentence}")
        return False
language = 'indonesia'
def get_random_question(language):
    if language == 'inggris':
        filtered_df = df[(df['sent_eng'].str.split().apply(len) > 3) & (df['sent_eng'].str.len() > 0)]
        index = random.choice(filtered_df.index)
        return filtered_df['sent_indo'][index], filtered_df['sent_eng'][index]

    elif language == 'indonesia':
        filtered_df = df[(df['sent_indo'].str.split().apply(len) > 3) & (df['sent_indo'].str.len() > 0)]
        index = random.choice(filtered_df.index)
        return filtered_df['sent_eng'][index], filtered_df['sent_indo'][index]

original_sentence, correct_translation = get_random_question(language)
shuffled_sentence = create_shuffled_sentence(original_sentence)

print(f"\nKalimat dalam bahasa {language.capitalize()}:\n{correct_translation}")
print(f"\nRangkailah kata-kata berikut untuk membentuk kalimat yang benar:\n\n{shuffled_sentence}")

user_input = input("\nJawaban Anda: ")

# Praproses input jika diperlukan
input_data = tokenizer_eng.texts_to_sequences([user_input])
input_data = tf.keras.preprocessing.sequence.pad_sequences(input_data, maxlen=max_len_eng, padding='post')

# Set input tensor ke interpreter
input_tensor_index = interpreter.get_input_details()[0]['index']
interpreter.set_tensor(input_tensor_index, input_data)

# Lakukan inferensi
interpreter.invoke()

# Dapatkan hasil inferensi
output_data = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])[0]
predicted_index = np.argmax(output_data)
predicted_translation = tokenizer_indo.index_word.get(predicted_index, "Token tidak dikenali")

# def model_output():
#     response_data = {
#         "Original_sentence": original_sentence,
#         "Correct_translation": correct_translation,
#         "User_input": user_input,
#         "Ouput_data": output_data
#     }
#     print(jsonify(response_data))

