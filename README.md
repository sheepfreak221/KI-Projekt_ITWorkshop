# KI-Projekt aus dem IT-Workshop

Dieses Repository enthält alles, was du brauchst, um das KI-Projekt lokal am Rechner zu Betreiben. Dabei handelt es sich um eine Flask-basierte Webanwendung mit sieben verschiedenen KI-Modellen für Text- und Bildverarbeitung. Ideal für den Einsatz in Schulen und anderen Bildungseinrichtungen.

## Features

- **GPT-2 Textgenerator** - Textgenerierung mit KI (Englisch)
- **EasyOCR Texterkennung** - Texterkennung aus Bildern (Englisch)
- **DistilBERT Sentiment-Analyse** - Stimmungserkennung von Texten (Englisch)
- **BLIP Image Captioning** - Automatische Bildbeschreibungen (Englisch)
- **Real-ESRGAN Bildverbesserung** - Upscaling und Verbesserung von Bildern (optimiert für Anime/Manga)
- **Coqui TTS Text-to-Speech** - Natürliche Sprachausgabe in Deutsch (Tacotron2-Modell)
- **Stable Diffusion 1.5 Text-to-Image** - Bilderzeugung aus Textbeschreibungen 

## Screenshot

[*Das KI-Projekt im Einsatz – alle 7 Modelle in einer Übersicht*](Screenshots/ki-projekt-screenshot.png)

## Voraussetzungen

- **Linux (Ubuntu 22.04 LTS wird empfohlen)** - [Offizielle Download-Seite](https://releases.ubuntu.com/jammy/)
- Python 3.10 (wichtig! Coqui TTS benötigt Python 3.8-3.11 (daher Ubuntu 22.04!), mit 3.10.4 getestet)
- Nginx als Reverse-Proxy
- mind. 8GB RAM (für alle Modelle empfohlen)
- GPU optional (beschleunigt einige Modelle)

### Alternativen für Windows:
- WSL 2 (Windows Subsystem for Linux)
- Linux-VM (z.B. mit Qemu)
- Docker (für Fortgeschrittene)

## Installation

### 1. Abhängigkeiten installieren (Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx
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
wget https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-ubuntu.zip
unzip realesrgan-ncnn-vulkan-20220424-ubuntu.zip
cp ./realesrgan-ncnn-vulkan-20220424-ubuntu/realesrgan-ncnn-vulkan /srv/ki-projekt/
chmod +x /srv/ki-projekt/realesrgan-ncnn-vulkan

cp -r ./realesrgan-ncnn-vulkan-20220424-ubuntu/models /srv/ki-projekt/
```

### 6. Python Abhängigkeiten installieren

```bash
pip install --upgrade pip
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cpu
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
Flask==2.3.3
Werkzeug==2.3.7
transformers==4.36.2
easyocr==1.7.1
opencv-python==4.9.0.80
Pillow==10.1.0
numpy==1.22.0
TTS==0.22.0
pydub==0.25.1
diffusers==0.30.3
```

## Verzeichnisstruktur nach der Installation

```
/srv/ki-projekt/
├── app.py                          # Hauptanwendung
├── realesrgan-ncnn-vulkan          # Real-ESRGAN ausführbare Datei
├── requirements.txt                # Python Abhängigkeiten
├── blueprints/                     # Blueprint-Module
│   ├── gpt2/                       # GPT-2 Textgenerator
│   │   ├── init.py
│   │   └── routes.py
│   ├── ocr/                        # EasyOCR Texterkennung
│   │   ├── init.py
│   │   └── routes.py
│   ├── bert/                       # DistilBERT Sentiment-Analyse
│   │   ├── init.py
│   │   └── routes.py
│   ├── blip/                       # BLIP Image Captioning
│   │   ├── init.py
│   │   └── routes.py
│   ├── realesrgan/                 # Real-ESRGAN Bildverbesserung
│   │   ├── init.py
│   │   └── routes.py
│   ├── coqui/                      # Coqui TTS Text zu Sprache
│   │   ├── init.py
│   │   └── routes.py
│   └── sd15/                       # Stable Diffusion 1.5 Text zu Bild
│       ├── init.py
│       └── routes.py
├── realesrgan_uploads/             # Temporäre Uploads für Real-ESRGAN
├── realesrgan_output/              # Verbesserte Bilder
├── coqui_uploads/                  # Temporäre Uploads für Coqui TTS
├── coqui_output/                   # Generierte Audiodateien
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
    ├── realesrgan.js
    ├── tts.js
    └── sd15.js

```

## API-Endpunkte


| App | Endpunkt | Methode | Beschreibung |
|-----|----------|---------|--------------|
| GPT-2 | `/gpt2/api/textgen/` | POST | Textgenerierung (Geschichten) |
| EasyOCR | `/ocr/api/ocr/upload-ocr` | POST | Texterkennung aus Bild |
| DistilBERT | `/bert/api/bert/chat` | POST | Sentiment-Analyse |
| BLIP | `/blip/api/blip/upload` | POST | Bildbeschreibung |
| Real-ESRGAN | `/realesrgan/api/process-image` | POST | Bildverbesserung |
| Real-ESRGAN | `/realesrgan/api/results/<filename>` | GET | Ergebnis abrufen |
| Coqui TTS | `/tts/api/tts/generate` | POST | Text-to-Speech (deutsch) |
| Coqui TTS | `/tts/api/tts/audio/<filename>` | GET | Generierte Audiodatei abrufen |
| Stable Diffusion 1.5 | `/sd15/api/generate` | POST | **Bildgenerierung aus Text (Base64)** |
| Stable Diffusion 1.5 | `/sd15/api/generate/file` | POST | **Bildgenerierung als Datei** |
| Stable Diffusion 1.5 | `/sd15/api/info` | GET | **Modell-Informationen** |






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

### Modelle & Bibliotheken
- [Hugging Face Transformers](https://github.com/huggingface/transformers) – DistilBERT (Sentiment-Analyse), GPT-2 (Textgenerierung), BLIP (Bildbeschreibung)
- [OpenAI](https://openai.com/research/gpt-2) – GPT-2 Textgenerierungsmodell
- [Salesforce](https://github.com/salesforce/BLIP) – BLIP Image Captioning
- [Coqui TTS](https://github.com/coqui-ai/TTS) – Text-to-Speech (Thorsten-Modell für Deutsch)
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) – Bildverbesserung
- [EasyOCR](https://github.com/JaidedAI/EasyOCR) – Texterkennung

### Frameworks & Tools
- [Flask](https://github.com/pallets/flask) – Webframework
- [PyTorch](https://github.com/pytorch/pytorch) – Machine-Learning-Framework
- [Nginx](https://nginx.org/) – Reverse-Proxy


## Zusätzlich benötigte Dateien:

**Nginx Konfiguration (`default`)**:

```nginx
server {
    listen 80;
    server_name <IP des Rechners>;

    client_max_body_size 50M;

    # Statische Startseite
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
        proxy_read_timeout 120s;
    }

    location /sd15/ {
        proxy_pass http://127.0.0.1:5000/sd15/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 350s;
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

    location /tts/ {
        proxy_pass http://127.0.0.1:5000/tts/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 120s;
    }

}
```
