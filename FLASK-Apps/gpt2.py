from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS aktivieren

# Lade die 124M-Version von GPT-2
text_generator = pipeline("text-generation", model="gpt2")

@app.route('/api/textgen/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # JSON-Daten erhalten
        data = request.get_json()
        
        # Überprüfen, ob die Daten gültig sind
        if not data or 'user_input' not in data:
            return jsonify({'error': 'Invalid input'}), 400  # Fehlerbehandlung für ungültige Eingaben
        
        user_input = data['user_input']  # 'user_input' aus den Daten extrahieren

        # Textgenerierung
        generated_text = text_generator(user_input, max_length=250, num_return_sequences=1)[0]['generated_text']

        # Antwort als JSON zurückgeben
        return jsonify({'generated_text': generated_text})

    # Für GET-Anfragen eine einfache Nachricht zurückgeben
    return jsonify({'message': 'Send a POST request with user_input.'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)