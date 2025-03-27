from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from flask_cors import CORS

# Flask-App initialisieren
app = Flask(__name__)
CORS(app)  # CORS aktivieren
UPLOAD_FOLDER = '/home/workshop/kiprojekt/html/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lade das BLIP-Modell und den Prozessor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route('/api/blip/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'Kein Bild hochgeladen'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'Kein Bild ausgewählt'}), 400

    prompt = request.form.get('prompt')

    filename = secure_filename(image.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)

    try:
        raw_image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print("Fehler beim Laden des Bildes:", e)
        return jsonify({'error': 'Fehler beim Laden des Bildes'}), 500

    inputs = processor(raw_image, text=prompt, return_tensors="pt") if prompt else processor(raw_image, return_tensors="pt")

    try:
        with torch.no_grad():
            output = model.generate(**inputs)
        description = processor.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        print("Fehler bei der Generierung der Beschreibung:", e)
        return jsonify({'error': 'Fehler bei der Generierung der Beschreibung'}), 500

    try:
        os.remove(image_path)
    except Exception as e:
        print("Fehler beim Löschen des Bildes:", e)

    return jsonify({'description': description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)