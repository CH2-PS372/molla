import os
import uuid
from flask import Flask, request, jsonify, abort
from inference import get_random_question, create_shuffled_sentence, evaluate_user_input

app = Flask(__name__)

# Dictionary to store question IDs and their corresponding sentences
question_data = {}

def get_quiz_param():
    try:
        language = request.args.get('language')
        if language is None:
            abort(400, description="Missing language parameter in request URL")
        return language
    except Exception as e:
        abort(400, description=str(e))

def get_questions_param():
    try:
        question_id = request.args.get('question_id')
        if question_id is None:
            abort(400, description="Missing question_id parameter in request URL")
        return question_id
    except Exception as e:
        abort(400, description=str(e))

@app.route("/quiz", methods=["GET"])
def quiz():
    if request.method == "GET":
        try:
            language = get_quiz_param()
            original_sentence, correct_translation = get_random_question(language)
            shuffled_sentence = create_shuffled_sentence(original_sentence)
            
            # Generate a random question ID using uuid
            question_id = str(uuid.uuid4())

            # Store question ID and original sentence in the dictionary
            question_data[question_id] = original_sentence

            response_data = {
                'question_id': question_id,
                'question_data': question_data,
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

@app.route("/questions", methods=["GET"])
def questions():
    try:
        response_data = {
            "question_data": question_data
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/questions", methods=["DELETE"])
def questions_delete():
    try:
        question_id = get_questions_param()
        if question_id not in question_data:
            return jsonify({"error": f"Invalid question_id: {question_id}"}), 400

        question_data.pop(question_id)
        response_data = {
            "status": "deletion success",
            "question_id": question_id
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0')
