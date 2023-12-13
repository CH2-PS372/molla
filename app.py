import os
import uuid
from flask import Flask, request, jsonify, abort
from inference import get_random_question, create_shuffled_sentence, evaluate_user_input

app = Flask(__name__)

# Dictionary to store question IDs and their corresponding sentences
question_data = {}

def parameter_check():
    try:
        data = request.get_json()
        language = data.get('language')
        if language is None:
            abort(400, description="Missing language parameter in request body")
        return language
    except Exception as e:
        abort(400, description=str(e))

@app.route("/quiz", methods=["GET"])
def quiz():
    if request.method == "GET":
        try:
            language = parameter_check()
            original_sentence, correct_translation = get_random_question(language)
            shuffled_sentence = create_shuffled_sentence(original_sentence)
            
            # Generate a random question ID using uuid
            question_id = str(uuid.uuid4())

            # Store question ID and original sentence in the dictionary
            question_data[question_id] = original_sentence

            response_data = {
                'question_id': question_id,
                'sentence': {
                    'original_sentence': original_sentence,
                    'correct_translation': correct_translation,
                    'shuffled_sentence': shuffled_sentence
                }
            }
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route("/quiz", methods=["POST"])
def evaluate():
    try:
        data = request.get_json()
        question_id = data.get('question_id')
        user_answer = data.get('user_answer')

        # Retrieve the original sentence for the given question ID
        original_sentence = question_data.get(question_id)

        if original_sentence is not None:
            # Evaluate the user's answer
            result = evaluate_user_input(user_answer, original_sentence)
            question_data.pop(question_id)

            return jsonify({"result": result})
        else:
            return jsonify({"error": f"Invalid question_id: {question_id}"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')