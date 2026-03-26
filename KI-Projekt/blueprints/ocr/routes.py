from flask import Blueprint, request, jsonify, current_app
import numpy as np
import cv2

ocr_bp = Blueprint('ocr', __name__)

# Reader global initialisieren (nur einmal)
def get_ocr_reader():
    if 'ocr_reader' not in current_app.config:
        import easyocr
        current_app.config['ocr_reader'] = easyocr.Reader(['de', 'en'])
    return current_app.config['ocr_reader']

@ocr_bp.route('/api/ocr/upload-ocr', methods=['POST'])
def upload_ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    
    try:
        # Bild direkt aus dem Speicher verarbeiten
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Text erkennen (gecachter Reader)
        reader = get_ocr_reader()
        results = reader.readtext(img)
        extracted_text = "\n".join([result[1] for result in results])
        
        return jsonify({
            'text': extracted_text,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500
