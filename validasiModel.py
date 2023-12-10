import pandas as pd
import random
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer

dataset_path = 'dataUji.tsv'
df = pd.read_csv(dataset_path, sep='\t', header=None, names=['num_eng', 'sent_eng', 'num_indo', 'sent_indo'])

model_path = 'nama_model.h5'
model = load_model(model_path)

tokenizer_eng = Tokenizer()
tokenizer_eng.fit_on_texts(df['sent_eng'])
max_len_eng = max([len(seq) for seq in tokenizer_eng.texts_to_sequences(df['sent_eng'])])
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

def get_random_question(language):
    if language == 'inggris':
        filtered_df = df[(df['sent_eng'].str.split().apply(len) > 3) & (df['sent_eng'].str.len() > 0)]
        index = random.choice(filtered_df.index)
        return filtered_df['sent_indo'][index], filtered_df['sent_eng'][index]

    elif language == 'indonesia':
        filtered_df = df[(df['sent_indo'].str.split().apply(len) > 3) & (df['sent_indo'].str.len() > 0)]
        index = random.choice(filtered_df.index)
        return filtered_df['sent_eng'][index], filtered_df['sent_indo'][index]


print("\nPilih bahasa untuk pertanyaan:")
print("1. Bahasa Indonesia")
print("2. Bahasa Inggris")
choice = input("Masukkan pilihan (1/2): ")

if choice == '1':
    language = 'inggris'
elif choice == '2':
    language = 'indonesia'
else:
    print("Pilihan tidak valid. Silakan masukkan pilihan yang benar.")
    exit()

while True:
    original_sentence, correct_translation = get_random_question(language)
    shuffled_sentence = create_shuffled_sentence(original_sentence)

    print(f"\nKalimat dalam bahasa {language.capitalize()}:\n{correct_translation}")
    print(f"\nRangkailah kata-kata berikut untuk membentuk kalimat yang benar:\n\n{shuffled_sentence}")

    user_input = input("\nJawaban Anda: ")

    if evaluate_user_input(user_input, original_sentence):
        continue_or_exit = input("\nApakah Anda ingin melanjutkan? (y/n): ")
        if continue_or_exit.lower() != 'y':
            break

print("Selesai. Terima kasih!")
