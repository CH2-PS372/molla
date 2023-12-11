import json
import os
from text_extracting import read_image_and_extract_text, translate_to_indonesian
from flask import Flask, request, jsonify
from sentence_h5 import get_random_question

app = Flask(__name__)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if request.method == "GET":
        try:
            language = 'indonesia'
            original_sentence, correct_translation = get_random_question(language)
            response_data = {
                'sentence': {
                    'lang_eng': original_sentence,
                    'lang_id': correct_translation
                }
            }
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)})

    return "OK"

@app.route('/translate', methods = ["GET", "POST"])
def translate():
    if request.method == "GET":
        # file = request.files.get('file')
        # if file is None or file.filename == "":
        #     return jsonify({"error": "no file"})
        try:
            image = "image1.png"
            image_path = os.path.join('images', image)
            extracted_text = read_image_and_extract_text(image_path)
            translated_text = translate_to_indonesian(extracted_text)
            response_data = {
                "extracted_text": str(extracted_text),
                "translated_text": str(translated_text)
            }
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)})
    return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3003)