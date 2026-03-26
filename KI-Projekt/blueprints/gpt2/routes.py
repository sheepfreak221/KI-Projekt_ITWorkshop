# blueprints/gpt2/routes.py (GPT-2 Large)
from flask import Blueprint, request, jsonify, current_app
from transformers import pipeline

gpt2_bp = Blueprint('gpt2', __name__)

def get_text_generator():
    if 'text_generator' not in current_app.config:
        print("Loading GPT-2 Large... (first start takes a moment)")
        current_app.config['text_generator'] = pipeline("text-generation", model="gpt2-medium")
        print("GPT-2 Large loaded!")
    return current_app.config['text_generator']

def words_to_tokens(word_count):
    return int(word_count * 1.3) + 20

@gpt2_bp.route('/api/textgen/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'user_input' not in data:
            return jsonify({'error': 'Invalid input'}), 400
        
        user_input = data['user_input']
        mode = data.get('mode', 'normal')
        max_words = data.get('max_words', None)
        
        try:
            text_generator = get_text_generator()
            
            if mode == 'story':
                if max_words and max_words > 0:
                    max_tokens = words_to_tokens(max_words)
                else:
                    max_tokens = 250
                
                # Prompt ist der Satz selbst + Leerzeichen
                prompt = user_input + " "
                
                generated = text_generator(
                    prompt,
                    max_new_tokens=max_tokens,
                    temperature=0.75,
                    do_sample=True,
                    top_p=0.9,
                    truncation=True,
                    pad_token_id=50256,
                    repetition_penalty=1.15
                )[0]['generated_text']
                
                # Komplette Geschichte inklusive Anfangssatz
                return jsonify({'generated_text': generated, 'model': 'gpt2-medium'})
            else:
                generated = text_generator(
                    user_input,
                    max_new_tokens=150,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=50256
                )[0]['generated_text']
                return jsonify({'generated_text': generated, 'model': 'gpt2-medium'})
            
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Send a POST request with user_input.'})