document.getElementById('ocrForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('ocrImage');
    const imageContainer = document.getElementById('ocrImageContainer');
    const resultContainer = document.getElementById('ocrResult');
    
    // Clear previous results
    resultContainer.textContent = '';
    imageContainer.innerHTML = '';
    
    if (fileInput.files.length === 0) {
        alert('Bitte wähle ein Bild aus!');
        return;
    }
    
    const file = fileInput.files[0];
    
    // Bild vorab anzeigen
    const reader = new FileReader();
    reader.onload = function(e) {
        imageContainer.innerHTML = `
            <img src="${e.target.result}" class="img-fluid" alt="Hochgeladenes Bild">
        `;
    };
    reader.readAsDataURL(file);
    
    // FormData für den Upload vorbereiten
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        resultContainer.textContent = 'Text wird erkannt...';
        
        const response = await fetch('/api/ocr/upload-ocr', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            resultContainer.textContent = data.text;
        } else {
            throw new Error(data.error || 'Fehler bei der Texterkennung');
        }
    } catch (error) {
        resultContainer.textContent = `Fehler: ${error.message}`;
        console.error('Fehler:', error);
    }
});