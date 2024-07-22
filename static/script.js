document.addEventListener('DOMContentLoaded', function () {
    const translateForm = document.getElementById('translate-form');
    const speakForm = document.getElementById('speak-form');
    const speechToTextForm = document.getElementById('speech-to-text-form');

    translateForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const text = document.getElementById('text-to-translate').value;
        const targetLanguage = document.getElementById('target-language').value;

        const response = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, target_language: targetLanguage })
        });
        const data = await response.json();
        document.getElementById('translation-result').innerText = data.translated_text || 'Translation failed';
    });

    speakForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const text = document.getElementById('text-to-speak').value;

        const response = await fetch('/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        const audio = new Audio(`data:audio/mp3;base64,${data.audio}`);
        audio.play();
    });

    speechToTextForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const audioFile = document.getElementById('audio-file').files[0];

        const formData = new FormData();
        formData.append('audio', audioFile);

        const response = await fetch('/speech-to-text', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        document.getElementById('transcript-result').innerText = data.transcript || 'Speech recognition failed';
    });
});
