# KI-Projekt aus dem IT-Workshop

Dieses Repository enthält alles, was du brauchst, um das KI-Projekt lokal am Rechner zu Betreiben. Dabei handelt es sich um eine Flask-basierte Webanwendung mit fünf verschiedenen KI-Modellen für Text- und Bildverarbeitung. Ideal für den Einsatz in Schulen und anderen Bildungseinrichtungen.

## Features

- **GPT-2 Textgenerator** - Textgenerierung mit KI (Englisch)
- **EasyOCR Texterkennung** - Texterkennung aus Bildern (Englisch)
- **DistilBERT Sentiment-Analyse** - Stimmungserkennung von Texten (Englisch)
- **BLIP Image Captioning** - Automatische Bildbeschreibungen (Englisch)
- **Real-ESRGAN Bildverbesserung** - Upscaling und Verbesserung von Bildern

## Voraussetzungen

- **Linux (z.B. Debian) wird dringend empfohlen**
- Python 3.8 oder höher
- Nginx als Reverse-Proxy
- mind. 8GB RAM (für alle Modelle empfohlen)
- GPU optional (beschleunigt einige Modelle)

### Alternativen für Windows:
- WSL 2 (Windows Subsystem for Linux)
- Linux-VM (z.B. mit Qemu)
- Docker (für Fortgeschrittene)

## Installation

### 1. System abhängigkeiten installieren (Debian)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx screen
```

### 2. Verzeichnisse erstellen und die Berechtigungen setzen

```bash
sudo mkdir -p /srv/www
sudo chown www-data:$USER /srv/www
sudo chmod 775 /srv/www

sudo mkdir -p /srv/ki-projekt
sudo chown $USER:$USER /srv/ki-projekt
```

### 3. Virtuelle Umgebung einrichten

```bash
cd /srv/ki-projekt
python3 -m venv venv
source venv/bin/activate
```



### 4. Klonen des Repository und kopieren der Dateien
```bash
cd $HOME
git clone https://github.com/sheepfreak221/KI-Projekt_ITWorkshop
cp KI-Projekt_ITWorkshop/Interface/* /srv/www/
cp KI-Projekt_ITWorkshop/KI-Projekt/* /srv/ki-projekt
```

### 5. Real-ESRGAN einrichten

Die ausführbare Datei realesrgan-ncnn-vulkan muss im Hauptverzeichnis liegen.
```bash
# Download (Beispiel für Linux x86_64)
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
unzip realesrgan-ncnn-vulkan-20220424-ubuntu.zip
mv ./realesrgan-ncnn-vulkan-20220424-ubuntu/realesrgan-ncnn-vulkan /srv/ki-projekt/
chmod +x /srv/ki-projekt/realesrgan-ncnn-vulkan

cp -r ./realesrgan-ncnn-vulkan-20220424-ubuntu/models /srv/ki-projekt/
```

### 6. Python Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### 7. Nginx konfigurieren

Die Nginx-Konfigurationsdatei in das richtige Verzeichnis kopieren:

```bash
sudo cp default /etc/nginx/sites-available/default
sudo nginx -t  # Testen der Konfiguration
sudo systemctl restart nginx
```

### 8. Anwendung starten

```bash
python app.py
```

Die Anwendung läuft jetzt unter `http://<IP des Rechners>/`

Der erste Start kann je nach Internetgeschwindigkeit 5-15 Minuten dauern (Download der KI-Modelle).

## Abhängigkeiten (requirements.txt)

```bash
Flask
Werkzeug
transformers
easyocr
opencv-python
Pillow
numpy
```

## Verzeichnisstruktur nach der Installation

```
/srv/ki-projekt/
├── app.py                          # Hauptanwendung
├── realesrgan-ncnn-vulkan          # Real-ESRGAN ausführbare Datei
├── requirements.txt                # Python Abhängigkeiten
├── blueprints/                     # Blueprint-Module
│   ├── gpt2/                       # GPT-2 Textgenerator
│   │   ├── __init__.py
│   │   └── gpt2_routes.py
│   ├── ocr/                        # EasyOCR Texterkennung
│   │   ├── __init__.py
│   │   └── ocr_routes.py
│   ├── bert/                       # DistilBERT Sentiment-Analyse
│   │   ├── __init__.py
│   │   └── bert_routes.py
│   ├── blip/                        # BLIP Image Captioning
│   │   ├── __init__.py
│   │   └── blip_routes.py
│   └── realesrgan/                 # Real-ESRGAN Bildverbesserung
│       ├── __init__.py
│       └── realesrgan_routes.py
├── realesrgan_uploads/             # Temporäre Uploads für Real-ESRGAN
├── realesrgan_output/              # Verbesserte Bilder
└── venv/                           # Python virtuelle Umgebung

/srv/www/
├── index.html                      # Startseite
├── css/
│   ├── bootstrap.min.css
│   └── style.css
└── js/
    ├── blip.js
    ├── distilbert.js
    ├── easyocr.js
    ├── gpt2.js
    └── realesrgan.js

```

## API-Endpunkte

| App | Endpunkt | Methode | Beschreibung |
|-----|----------|---------|--------------|
| GPT-2 | `/gpt2/api/textgen/` | POST | Textgenerierung |
| EasyOCR | `/ocr/api/ocr/upload-ocr` | POST | Texterkennung aus Bild |
| DistilBERT | `/bert/api/bert/chat` | POST | Sentiment-Analyse |
| BLIP | `/blip/api/blip/upload` | POST | Bildbeschreibung |
| Real-ESRGAN | `/realesrgan/api/process-image` | POST | Bildverbesserung |
| Real-ESRGAN | `/realesrgan/api/results/<filename>` | GET | Ergebnis abrufen |


## Wichtige Hinweise

- **Modelle werden beim ersten Start automatisch heruntergeladen** (ca. 2-3GB Gesamtgröße)
- Der erste Start kann einige Minuten dauern
- Real-ESRGAN benötigt die ausführbare Datei im Hauptverzeichnis
- Alle Uploads werden temporär gespeichert und nach Verarbeitung gelöscht

## Sicherheitshinweise für Schulen

- Die Anwendung läuft auf `127.0.0.1:5000` und ist nur über Nginx erreichbar
- Nginx dient als Reverse-Proxy und kann bei Bedarf mit SSL (Let's Encrypt) abgesichert werden
- Alle Uploads werden nach Verarbeitung gelöscht

## Lizenz

Dieses Projekt ist für Bildungszwecke gedacht. Die verwendeten Modelle unterliegen ihren eigenen Lizenzen.

## Danksagung

- [Hugging Face](https://huggingface.co/) für die Transformer-Modelle
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) für die Bildverbesserung
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) für die Texterkennung


## Zusätzlich benötigte Dateien:

**Nginx Konfiguration (`default`)**:

```nginx
server {
    listen 80;
    server_name <IP des Rechners>;
    
    client_max_body_size 50M;
    
    location / {
        root /srv/www;
        try_files $uri $uri/ /index.html;
        expires 1h;
        add_header Cache-Control "public, immutable";
    }
    
    location /gpt2/ {
        proxy_pass http://127.0.0.1:5000/gpt2/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /ocr/ {
        proxy_pass http://127.0.0.1:5000/ocr/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 60s;
    }
    
    location /bert/ {
        proxy_pass http://127.0.0.1:5000/bert/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /blip/ {
        proxy_pass http://127.0.0.1:5000/blip/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 60s;
    }
    
    location /realesrgan/ {
        proxy_pass http://127.0.0.1:5000/realesrgan/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 120s;
    }
}
```
