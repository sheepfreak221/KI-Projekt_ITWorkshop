async function generateSpeech() {
    const text = document.getElementById('tts-text').value;
    const resultDiv = document.getElementById('tts-result');
    
    if (!text.trim()) {
        resultDiv.innerHTML = '<div class="alert alert-warning">Bitte gib einen Text ein.</div>';
        return;
    }
    
    resultDiv.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-spinner fa-spin"></i> Generiere Sprache...
        </div>
    `;
    
    try {
        const response = await fetch('/tts/api/tts/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        console.log('Status:', response.status);
        console.log('Status Text:', response.statusText);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        console.log('Data:', data);
        
        if (data.status === 'success') {
            resultDiv.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> ${data.message}
                </div>
                <div class="card mt-2">
                    <div class="card-body">
                        <h6 class="card-title">Audio-Player:</h6>
                        <audio controls class="w-100" autoplay>
                            <source src="/tts/api/tts/audio/${data.audio_file}" type="audio/wav">
                            Dein Browser unterstützt keinen Audio-Player.
                        </audio>
                        <div class="mt-2">
                            <a href="/tts/api/tts/audio/${data.audio_file}" class="btn btn-sm btn-outline-primary" download>
                                <i class="fas fa-download"></i> Audio herunterladen
                            </a>
                        </div>
                    </div>
                </div>
            `;
        } else {
            throw new Error(data.error || 'Unbekannter Fehler');
        }
    } catch (error) {
        console.error('Fehler:', error);
        resultDiv.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle"></i> Fehler: ${error.message}
            </div>
        `;
    }
}