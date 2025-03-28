from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Konfiguration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

# Verzeichnisse erstellen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/process-image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify({'error': 'Keine Datei hochgeladen'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Keine Datei ausgewählt'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Nur folgende Dateitypen erlaubt: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400

    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = f'enhanced_{filename}'
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        file.save(input_path)

        cmd = [
            './realesrgan-ncnn-vulkan',
            '-i', input_path,
            '-o', output_path
        ]
        
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        
        if not os.path.exists(output_path):
            raise FileNotFoundError(f"Output file was not created at {output_path}")
        
        return jsonify({
            'status': 'success',
            'enhanced_image': output_filename
        })
        
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'Bildverarbeitung fehlgeschlagen',
            'details': e.stderr
        }), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results/<filename>')
def get_result(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)  # Port auf 5000 geändert für Nginx
