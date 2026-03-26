from flask import Blueprint, request, jsonify, send_from_directory, current_app
import os
import re
from werkzeug.utils import secure_filename

coqui_bp = Blueprint('coqui', __name__)

ALLOWED_EXTENSIONS = {'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_tts_model():
    if 'coqui_tts' not in current_app.config:
        from TTS.api import TTS
        current_app.config['coqui_tts'] = TTS("tts_models/de/thorsten/tacotron2-DDC", gpu=False)
    return current_app.config['coqui_tts']

def clean_text(text):
    replacements = {
        "…": "...",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r"\s*\n\s*", " ", text)
    return text.strip()

@coqui_bp.route('/api/tts/generate', methods=['POST'])
def generate_speech():
    # Prüfen ob Text direkt übergeben wurde
    if 'text' in request.json:
        text = request.json.get('text', '')
        if not text:
            return jsonify({'error': 'Kein Text angegeben'}), 400
        
        try:
            output_folder = os.path.join(current_app.root_path, 'coqui_output')
            os.makedirs(output_folder, exist_ok=True)
            
            output_filename = f"speech_{hash(text) % 1000000}.wav"
            output_path = os.path.join(output_folder, output_filename)
            
            tts = get_tts_model()
            tts.tts_to_file(text=text, file_path=output_path)
            
            return jsonify({
                'status': 'success',
                'audio_file': output_filename,
                'message': 'Sprache erfolgreich generiert'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # Prüfen ob Datei hochgeladen wurde
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Nur .txt Dateien erlaubt'}), 400
        
        try:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'coqui_uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            input_path = os.path.join(upload_folder, filename)
            file.save(input_path)
            
            # Text aus Datei lesen
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            text = clean_text(text)
            
            output_folder = os.path.join(current_app.root_path, 'coqui_output')
            os.makedirs(output_folder, exist_ok=True)
            
            output_filename = f"speech_{filename.replace('.txt', '')}.wav"
            output_path = os.path.join(output_folder, output_filename)
            
            tts = get_tts_model()
            tts.tts_to_file(text=text, file_path=output_path)
            
            # Temporäre Datei löschen
            os.remove(input_path)
            
            return jsonify({
                'status': 'success',
                'audio_file': output_filename,
                'message': 'Sprache erfolgreich generiert'
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    else:
        return jsonify({'error': 'Weder Text noch Datei angegeben'}), 400

@coqui_bp.route('/api/tts/audio/<filename>')
def get_audio(filename):
    output_folder = os.path.join(current_app.root_path, 'coqui_output')
    return send_from_directory(output_folder, filename)

@coqui_bp.route('/api/tts/languages', methods=['GET'])
def get_languages():
    return jsonify({
        'languages': [
            {'code': 'de', 'name': 'Deutsch', 'model': 'tts_models/de/thorsten/tacotron2-DDC'},
            {'code': 'en', 'name': 'Englisch', 'model': 'tts_models/en/ljspeech/tacotron2-DDC'},
            {'code': 'fr', 'name': 'Französisch', 'model': 'tts_models/fr/css10/tts'}
        ]
    })
