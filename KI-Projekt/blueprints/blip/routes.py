from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from PIL import Image
import torch

blip_bp = Blueprint('blip', __name__)

# BLIP Modell und Processor einmalig laden und cachen
def get_blip_model():
    if 'blip_processor' not in current_app.config:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        
        current_app.config['blip_processor'] = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        current_app.config['blip_model'] = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    return current_app.config['blip_model'], current_app.config['blip_processor']

@blip_bp.route('/api/blip/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'Kein Bild hochgeladen'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'Kein Bild ausgewählt'}), 400

    prompt = request.form.get('prompt')
    
    # Temporären Upload-Ordner für diese App
    upload_folder = os.path.join(current_app.root_path, 'blip_uploads')
    os.makedirs(upload_folder, exist_ok=True)

    filename = secure_filename(image.filename)
    image_path = os.path.join(upload_folder, filename)
    image.save(image_path)

    try:
        raw_image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print("Fehler beim Laden des Bildes:", e)
        return jsonify({'error': 'Fehler beim Laden des Bildes'}), 500

    # Modell und Processor laden
    model, processor = get_blip_model()
    
    # Input vorbereiten
    if prompt:
        inputs = processor(raw_image, text=prompt, return_tensors="pt")
    else:
        inputs = processor(raw_image, return_tensors="pt")

    try:
        with torch.no_grad():
            output = model.generate(**inputs)
        description = processor.decode(output[0], skip_special_tokens=True)
    except Exception as e:
        print("Fehler bei der Generierung der Beschreibung:", e)
        return jsonify({'error': 'Fehler bei der Generierung der Beschreibung'}), 500

    # Temporäres Bild löschen
    try:
        os.remove(image_path)
    except Exception as e:
        print("Fehler beim Löschen des Bildes:", e)

    return jsonify({'description': description})
