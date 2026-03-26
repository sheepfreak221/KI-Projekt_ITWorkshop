from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os
import subprocess
from werkzeug.utils import secure_filename

realesrgan_bp = Blueprint('realesrgan', __name__)

# Konfiguration
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_upload_folder():
    upload_folder = os.path.join(current_app.root_path, 'realesrgan_uploads')
    os.makedirs(upload_folder, exist_ok=True)
    return upload_folder

def get_output_folder():
    output_folder = os.path.join(current_app.root_path, 'realesrgan_output')
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

@realesrgan_bp.route('/api/process-image', methods=['POST'])
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
        upload_folder = get_upload_folder()
        output_folder = get_output_folder()
        
        input_path = os.path.join(upload_folder, filename)
        output_filename = f'enhanced_{filename}'
        output_path = os.path.join(output_folder, output_filename)
        
        file.save(input_path)

        # Pfad zum realesrgan Tool (muss im Hauptverzeichnis liegen)
        realesrgan_path = os.path.join(current_app.root_path, 'realesrgan-ncnn-vulkan')
        
        cmd = [
            realesrgan_path,
            '-i', input_path,
            '-o', output_path
        ]
        
        subprocess.run(
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

@realesrgan_bp.route('/api/results/<filename>')
def get_result(filename):
    output_folder = get_output_folder()
    return send_from_directory(output_folder, filename)
