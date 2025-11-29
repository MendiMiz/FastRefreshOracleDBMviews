// Contenuto del file: static/js/script.js (versione temporanea per debug)

// Funzione JavaScript per gestire il refresh tramite API
async function handleRefresh(method) {
    const statusArea = document.getElementById('refresh-status');
    statusArea.innerHTML = `Avvio refresh ${method === 'F' ? 'FAST' : 'COMPLETE'}...`;

    try {
        const response = await fetch('/refresh_mv', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ method: method })
        });

        const data = await response.json();

        if (data.status === 'success') {
            statusArea.innerHTML = `✅ Refresh ${data.method === 'F' ? 'FAST' : 'COMPLETE'} completato in: <strong>${data.duration} secondi</strong>. Ricarico la pagina...`;

            // RIGA SPOSTATA FUORI DALL'IF

        } else {
            statusArea.innerHTML = `❌ Errore durante il refresh: ${data.message}`;
        }

        // QUESTA RIGA ORA VIENE ESEGUITA SEMPRE DOPO LA CHIAMATA API
        location.reload();

    } catch (error) {
        // Se c'è un errore di connessione, mostralo e NON ricaricare immediatamente
        statusArea.innerHTML = `❌ Errore di connessione: ${error}`;
    }
}
