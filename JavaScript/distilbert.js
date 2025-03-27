document.getElementById('textForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = document.getElementById('textInput_senti').value;
    
    // Überprüfen, ob Text leer ist
    if (!text) {
        alert("Bitte gib einen Text ein!");
        return; // Abbruch, wenn kein Text vorhanden
    }
    

    const response = await fetch('/api/bert/chat', {  // Geändert zu NGINX-Route
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: text })
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error('Fehler beim Senden des Textes:', errorText);
        document.getElementById('textResult_senti').innerText = 'Fehler beim Senden des Textes.';
        return;
    }

    const result = await response.json();
    document.getElementById('textResult_senti').innerText = `Sentiment: ${result.sentiment}`;
});