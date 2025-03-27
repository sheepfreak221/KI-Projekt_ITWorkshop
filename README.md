# KI-Projekt aus dem IT-Workshop

Dieses Repository enthält die FLASK-Apps der KI-Modelle aus unserem Workshop.

## Empfohlene Umgebung
**Linux (z.B. Debian) wird dringend empfohlen**

### Alternativen für Windows:
- WSL 2 (Windows Subsystem for Linux)
- Linux-VM (z.B. mit VirtualBox)
- Docker (für Fortgeschrittene)

## Voraussetzungen
- Python 3.8+
- pip
- virtualenv
- Nginx

## Installation der Modelle

### 1. BLIP (Image Captioning)

    # Umgebung erstellen
    python -m venv blip_env
    source blip_env/bin/activate  # Linux/Mac

    # Abhängigkeiten
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    pip install flask flask-cors transformers

### 2. EasyOCR (Texterkennung)

    python -m venv easyocr_env
    source easyocr_env/bin/activate
    
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
    pip install flask flask-cors easyocr opencv-python numpy

### 3. Real-ESRGAN (Bildverbesserung)

    python -m venv esrgan_env
    source esrgan_env/bin/activate
    
    pip install flask flask-cors
    # Binary von https://github.com/xinntao/Real-ESRGAN herunterladen

### 4. Distil-BERT (NLP)

    python -m venv bert_env
    source bert_env/bin/activate
    
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    pip install flask flask-cors transformers

### 5. GPT-2 (Textgenerierung)

    python -m venv gpt2_env
    source gpt2_env/bin/activate
    
    pip install torch --index-url https://download.pytorch.org/whl/cpu
    pip install flask flask-cors transformers 

## Nginx Einrichtung

    # Backup der originalen Konfiguration
    sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
    
    # Neue Konfiguration kopieren
    sudo cp path/to/your/default /etc/nginx/sites-available/
    
    # Konfiguration testen
    sudo nginx -t
    
    # Nginx neustarten
    sudo systemctl restart nginx

## Flask Apps starten
Für jedes Modell in der jeweiligen Umgebung:

    Kopiert die jeweilige FLASK-App einfach in die entsprechende Umgebung und startet sie, z.B. mit

	python BLIP.py


## Troubleshooting
- Nginx Logs: /var/log/nginx/error.log
- Port-Konflikte: netstat -tulnp