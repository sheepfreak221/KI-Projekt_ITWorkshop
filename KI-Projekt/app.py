from flask import Flask, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein-geheimer-schlüssel-für-die-schule'

# Blueprints importieren
from blueprints.gpt2.routes import gpt2_bp
from blueprints.ocr.routes import ocr_bp
from blueprints.bert.routes import bert_bp
from blueprints.blip.routes import blip_bp
from blueprints.realesrgan.routes import realesrgan_bp
from blueprints.coqui.routes import coqui_bp
from blueprints.sd15.routes import sd15_bp  

# Blueprints registrieren
app.register_blueprint(gpt2_bp, url_prefix='/gpt2')
app.register_blueprint(ocr_bp, url_prefix='/ocr')
app.register_blueprint(bert_bp, url_prefix='/bert')
app.register_blueprint(blip_bp, url_prefix='/blip')
app.register_blueprint(realesrgan_bp, url_prefix='/realesrgan')
app.register_blueprint(coqui_bp, url_prefix='/tts')
app.register_blueprint(sd15_bp, url_prefix='/sd15') 

@app.route('/')
def index():
    return jsonify({
        'apps': [
            {'name': 'GPT-2 Textgenerator', 'endpoint': '/gpt2/api/textgen/'},
            {'name': 'EasyOCR Texterkennung', 'endpoint': '/ocr/api/ocr/upload-ocr'},
            {'name': 'DistilBERT Sentiment-Analyse', 'endpoint': '/bert/api/bert/chat'},
            {'name': 'BLIP Image Captioning', 'endpoint': '/blip/api/blip/upload'},
            {'name': 'Real-ESRGAN Bildverbesserung', 'endpoint': '/realesrgan/api/process-image'},
            {'name': 'Coqui TTS', 'endpoint': '/tts/api/tts/generate'},
            {'name': 'Stable Diffusion 1.5', 'endpoint': '/sd15/api/generate'},  
        ]
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
