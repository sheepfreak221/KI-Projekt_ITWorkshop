document.addEventListener('DOMContentLoaded', function() {
    
    const textForm = document.getElementById('textForm_textgen');
    const textInput = document.getElementById('textInput_textgen');
    const textResult = document.getElementById('textResult_textgen');
    
    if (!textForm || !textInput || !textResult) return;
    
    textForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const text = textInput.value;
        
        if (!text.trim()) {
            alert("Bitte gib einen Satz als Anfang ein!");
            return;
        }
        
        textResult.innerHTML = `<div class="alert alert-info"><i class="fas fa-spinner fa-spin"></i> Generiere Geschichte mit GPT-2 Large... (ca. 10-15 Sekunden)</div>`;
        
        try {
            const response = await fetch('/gpt2/api/textgen/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_input: text, max_words: 150 })
            });
            
            if (!response.ok) {
                const errorText = await response.text();
                textResult.innerHTML = `<div class="alert alert-danger">Fehler: ${errorText}</div>`;
                return;
            }
            
            const result = await response.json();
            
            textResult.innerHTML = `
                <div class="alert alert-success">
                    <strong>Deine Geschichte:</strong><br>
                    <div class="story-text">${escapeHtml(result.generated_text)}</div>
                </div>
            `;
            
        } catch (error) {
            textResult.innerHTML = `<div class="alert alert-danger">Netzwerkfehler: ${error.message}</div>`;
        }
    });
    
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}