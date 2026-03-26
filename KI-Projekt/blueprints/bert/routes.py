from flask import Blueprint, request, jsonify, current_app
import torch

bert_bp = Blueprint('bert', __name__)

# Model und Tokenizer einmalig laden und cachen
def get_bert_model():
    if 'bert_model' not in current_app.config:
        from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
        
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        current_app.config['bert_tokenizer'] = DistilBertTokenizer.from_pretrained(model_name)
        current_app.config['bert_model'] = DistilBertForSequenceClassification.from_pretrained(model_name)
    
    return current_app.config['bert_model'], current_app.config['bert_tokenizer']

@bert_bp.route('/api/bert/upload', methods=['POST'])
def upload_image():
    return jsonify({'description': 'Bild erfolgreich hochgeladen!'})

@bert_bp.route('/api/bert/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    
    if not user_input:
        return jsonify({'error': 'Keine Nachricht empfangen'}), 400
    
    # Modell und Tokenizer laden
    model, tokenizer = get_bert_model()
    
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
