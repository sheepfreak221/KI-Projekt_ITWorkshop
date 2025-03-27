// Text an Flask senden
document.getElementById('textForm_textgen').addEventListener('submit', async (event) => {
    event.preventDefault();
    const text = document.getElementById('textInput_textgen').value;

    // Überprüfen, ob Text leer ist
    if (!text) {
        alert("Bitte gib einen Text ein!");
        return; // Abbruch, wenn kein Text vorhanden
    }

    const response = await fetch('/api/textgen/', { // Geht jetzt über Nginx
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: text })
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error('Fehler beim Senden des Textes:', errorText);
        document.getElementById('textResult_textgen').innerText = 'Fehler beim Senden des Textes.';
        return;
    }

    const result = await response.json();

    // Ergebnis anzeigen
    document.getElementById('textResult_textgen').innerText = `Generierter Text: ${result.generated_text}`;
});