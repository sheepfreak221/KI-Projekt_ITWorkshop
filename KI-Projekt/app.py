from flask import Flask, jsonify
import os

app = Flask(__name__)

# Blueprints importieren
from blueprints.gpt2.routes import gpt2_bp
from blueprints.ocr.routes import ocr_bp
from blueprints.bert.routes import bert_bp
from blueprints.blip.routes import blip_bp
from blueprints.realesrgan.routes import realesrgan_bp
from blueprints.coqui.routes import coqui_bp

# Blueprints registrieren
app.register_blueprint(gpt2_bp, url_prefix='/gpt2')
app.register_blueprint(ocr_bp, url_prefix='/ocr')
app.register_blueprint(bert_bp, url_prefix='/bert')
app.register_blueprint(blip_bp, url_prefix='/blip')
app.register_blueprint(realesrgan_bp, url_prefix='/realesrgan')
app.register_blueprint(coqui_bp, url_prefix='/tts')

@app.route('/')
def index():
    return jsonify({
        'apps': [
            {'name': 'GPT-2 Textgenerator', 'endpoint': '/gpt2/api/textgen/'},
            {'name': 'EasyOCR Texterkennung', 'endpoint': '/ocr/api/ocr/upload-ocr'},
            {'name': 'DistilBERT Sentiment-Analyse', 'endpoint': '/bert/api/bert/chat'},
            {'name': 'BLIP Image Captioning', 'endpoint': '/blip/api/blip/upload'},
            {'name': 'Real-ESRGAN Bildverbesserung', 'endpoint': '/realesrgan/api/process-image'},
            {'name': 'Coqui TTS', 'endpoint': '/tts/api/tts/generate'}
        ]
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
