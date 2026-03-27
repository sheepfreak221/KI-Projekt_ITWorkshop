async function generateImage() {
    const prompt = document.getElementById('sd15-prompt').value;
    const negativePrompt = document.getElementById('sd15-negative').value;
    const resultDiv = document.getElementById('sd15-result');
    
    if (!prompt.trim()) {
        alert("Bitte gib einen Prompt ein!");
        return;
    }
    
    // Ladeanimation anzeigen
    resultDiv.innerHTML = `
        <div class="alert alert-info">
            <i class="fas fa-spinner fa-spin"></i> 
            Generiere Bild mit Stable Diffusion 1.5...<br>
            <small>Dauert ca. 3 Minuten (20 Schritte).</small>
        </div>
    `;
    
    const requestBody = {
        prompt: prompt,
        steps: 20  
    };
    
    if (negativePrompt.trim()) {
        requestBody.negative_prompt = negativePrompt;
    }
    
    try {
        const startTime = Date.now();
        
        const response = await fetch('/sd15/api/generate/file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            resultDiv.innerHTML = `<div class="alert alert-danger">Fehler: ${errorText}</div>`;
            return;
        }
        
        // Bild als Blob empfangen
        const blob = await response.blob();
        const imageUrl = URL.createObjectURL(blob);
        const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
        
        resultDiv.innerHTML = `
            <div class="alert alert-success">
                <strong>Bild generiert!</strong> (${elapsed} Sekunden)
            </div>
            <div class="text-center">
                <img src="${imageUrl}" class="img-fluid rounded border" alt="Generated image" style="max-width: 100%;">
                <div class="mt-2">
                    <a href="${imageUrl}" download="sd15_${Date.now()}.png" class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-download"></i> Bild herunterladen
                    </a>
                </div>
                <small class="text-muted d-block mt-2">Prompt: "${escapeHtml(prompt)}"</small>
            </div>
        `;
        
    } catch (error) {
        console.error('Fehler:', error);
        resultDiv.innerHTML = `<div class="alert alert-danger">Netzwerkfehler: ${error.message}</div>`;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}