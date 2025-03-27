from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import numpy as np
import cv2

app = Flask(__name__)
CORS(app, resources={r"/api/ocr/*": {"origins": "*"}})  # CORS für die API-Routen

# Initialize the EasyOCR reader
reader = easyocr.Reader(['de', 'en'])  # Deutsch und Englisch

@app.route('/api/ocr/upload-ocr', methods=['POST'])
def upload_ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    
    try:
        # Bild direkt aus dem Speicher verarbeiten (ohne Speicherung)
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        # Text erkennen
        results = reader.readtext(img)
        extracted_text = "\n".join([result[1] for result in results])
        
        return jsonify({
            'text': extracted_text,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(port=5005, debug=True)