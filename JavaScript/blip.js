document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    
    if (!uploadForm) {
        console.error('Formular mit ID "uploadForm" nicht gefunden!');
        return;
    }

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const imageInput = document.getElementById('image');
        const promptInput = document.getElementById('prompt');
        
        if (!imageInput || !imageInput.files[0]) {
            alert('Bitte wähle ein Bild aus!');
            return;
        }

        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
        if (promptInput && promptInput.value) {
            formData.append('prompt', promptInput.value);
        }

        try {
            const response = await fetch('/api/blip/upload', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error(await response.text());

            const result = await response.json();

            // Bild anzeigen
            const imageContainer = document.getElementById('imageContainer');
            const resultElement = document.getElementById('result');
            
            if (imageContainer) {
                imageContainer.innerHTML = '';
                const imgElement = document.createElement('img');
                imgElement.src = URL.createObjectURL(imageInput.files[0]);
                imgElement.alt = "Hochgeladenes Bild";
                imgElement.style.maxWidth = "200px";
                imgElement.classList.add('shadow');
                imageContainer.appendChild(imgElement);
            }

            if (resultElement) {
                resultElement.innerText = result.description 
                    ? "Bildbeschreibung: " + result.description
                    : 'Keine Beschreibung erhalten.';
            }
        } catch (error) {
            console.error('Fehler:', error);
            alert('Ein Fehler ist aufgetreten: ' + error.message);
        }
    });
});