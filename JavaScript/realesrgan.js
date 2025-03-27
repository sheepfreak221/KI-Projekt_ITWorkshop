async function processRealESRGAN() {
    const fileInput = document.getElementById('realesrgan-image');
    const resultContainer = document.getElementById('realesrgan-result');
    
    resultContainer.innerHTML = '<div class="loading-spinner">Verarbeite Bild...</div>';
    
    if (!fileInput.files.length) {
        resultContainer.innerHTML = '<p class="text-danger"></p>';
        alert("Bitte wähle ein Bild aus!");
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/api/process-image', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) throw new Error(data.error);
        
        const enhancedUrl = `/api/results/${data.enhanced_image}?t=${Date.now()}`;
        
        resultContainer.innerHTML = `
            <div class="result-fullsize">
                <h4 class="mb-3">Verbessertes Ergebnis</h4>
                <img src="${enhancedUrl}" class="enhanced-image">
                <div class="mt-3">
                    <a href="${enhancedUrl} target="_blank"" download class="btn btn-success">
                        Bild herunterladen
                    </a>
                </div>
            </div>
        `;
    } catch (error) {
        resultContainer.innerHTML = `<p class="text-danger">Fehler: ${error.message}</p>`;
    }
}