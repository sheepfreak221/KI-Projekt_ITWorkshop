from flask import Blueprint, request, jsonify, send_file, current_app
import torch
from diffusers import StableDiffusionPipeline
import io
import time
import base64
from PIL import Image

sd15_bp = Blueprint('sd15', __name__)

def get_sd_pipeline():
    if 'sd_pipe' not in current_app.config:
        print("Loading Stable Diffusion 1.5... (first start takes 2-3 minutes)")
        
        # Lade Modell mit float32 für CPU
        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float32,
            safety_checker=None,  # Deaktiviert Safety Checker für Geschwindigkeit
            requires_safety_checker=False
        )
        pipe = pipe.to("cpu")
        
        # Optimierungen für CPU
        pipe.enable_attention_slicing()  # Spart RAM
        
        current_app.config['sd_pipe'] = pipe
        print("Stable Diffusion 1.5 loaded!")
        
    return current_app.config['sd_pipe']

@sd15_bp.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400
    
    prompt = data['prompt']
    negative_prompt = data.get('negative_prompt', '')
    steps = data.get('steps', 25)  # Weniger Schritte für CPU
    guidance_scale = data.get('guidance_scale', 7.5)
    width = data.get('width', 512)
    height = data.get('height', 512)
    
    try:
        start_time = time.time()
        
        pipe = get_sd_pipeline()
        
        with torch.no_grad():
            image = pipe(
                prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=guidance_scale,
                width=width,
                height=height
            ).images[0]
        
        elapsed = time.time() - start_time
        
        # Bild als PNG in Bytes umwandeln
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Optional: Base64 für JSON-Antwort (falls gewünscht)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({
            'success': True,
            'image': img_base64,
            'time': round(elapsed, 2),
            'steps': steps,
            'prompt': prompt
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@sd15_bp.route('/api/generate/file', methods=['POST'])
def generate_file():
    """Alternative: Direkt als Datei zurückgeben"""
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400
    
    prompt = data['prompt']
    negative_prompt = data.get('negative_prompt', '')
    steps = data.get('steps', 25)
    
    try:
        pipe = get_sd_pipeline()
        
        with torch.no_grad():
            image = pipe(
                prompt,
                negative_prompt=negative_prompt,
                num_inference_steps=steps,
                guidance_scale=7.5
            ).images[0]
        
        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='sd15_generated.png'
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@sd15_bp.route('/api/info', methods=['GET'])
def info():
    return jsonify({
        'model': 'Stable Diffusion 1.5',
        'device': 'cpu',
        'supported_sizes': ['512x512'],
        'default_steps': 25,
        'estimated_time': '45-75 seconds per image'
    })