from flask import Flask, request, jsonify
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS aktivieren

# Modell und Tokenizer laden
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = DistilBertTokenizer.from_pretrained(model_name)
model = DistilBertForSequenceClassification.from_pretrained(model_name)

@app.route('/api/bert/upload', methods=['POST'])
def upload_image():
    return jsonify({'description': 'Bild erfolgreich hochgeladen!'})

@app.route('/api/bert/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    # Text tokenisieren
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)

    # Vorhersage durchführen
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Wahrscheinlichkeiten berechnen
    probabilities = torch.nn.functional.softmax(logits, dim=-1).numpy()[0]
    sentiment = "positive" if probabilities[1] > 0.5 else "negative"

    if sentiment == "positive":
        response = "I'm glad to hear that! How can I assist you further?"
    else:
        response = "I'm sorry to hear that. How can I help you?"

    return jsonify({'response': response, 'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)