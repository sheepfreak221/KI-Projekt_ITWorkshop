from flask import Blueprint, request, jsonify, current_app
from transformers import pipeline

gpt2_bp = Blueprint('gpt2', __name__)

# Globalen Pipeline-Cache vermeiden
def get_text_generator():
    if 'text_generator' not in current_app.config:
        current_app.config['text_generator'] = pipeline("text-generation", model="gpt2")
    return current_app.config['text_generator']

@gpt2_bp.route('/api/textgen/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'user_input' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        user_input = data['user_input']
        
        # Textgenerierung mit gecachtem Pipeline
        text_generator = get_text_generator()
        generated_text = text_generator(user_input, max_length=250, num_return_sequences=1)[0]['generated_text']

        return jsonify({'generated_text': generated_text})

    return jsonify({'message': 'Send a POST request with user_input.'})
