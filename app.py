from flask import Flask, request, jsonify, render_template
import requests
import pyttsx3
from vosk import Model, KaldiRecognizer
import json
import base64
import io
from langdetect import detect
import time

# Create Flask app instance
app = Flask(__name__)

# Set up pyttsx3 TTS
engine = pyttsx3.init()

# Load Vosk model for speech-to-text
model_path = "C:\\Tilak\\Hackathon\\Punt Partners\\language_translation_app\\model\\vosk-model-small-en-us-0.15"  # Path to the directory containing the Vosk model
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data['text']
    target_language = data['target_language']

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                'https://libretranslate.de/translate',
                data={
                    'q': text,
                    'source': 'auto',
                    'target': target_language,
                    'format': 'text'
                }
            )
            response.raise_for_status()  # Check if the request was successful

            print(f"Response status code: {response.status_code}")
            print(f"Response text: {response.text}")

            result = response.json()
            translated_text = result.get('translatedText', 'Translation error')
            return jsonify({'translated_text': translated_text})
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                return jsonify({'error': 'HTTP error occurred'}), 500
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
            else:
                return jsonify({'error': 'Request error occurred'}), 500
        except json.JSONDecodeError as json_err:
            print(f"JSON decode error occurred: {json_err}")
            print(f"Response text: {response.text}")
            return jsonify({'error': 'JSON decode error occurred'}), 500

@app.route('/speak', methods=['POST'])
def speak_text():
    data = request.json
    text = data['text']

    with io.BytesIO() as audio_file:
        engine.save_to_file(text, 'output.mp3')
        engine.runAndWait()
        with open('output.mp3', 'rb') as f:
            audio_content = base64.b64encode(f.read()).decode('utf-8')

    return jsonify({'audio': audio_content})

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    audio_file = request.files['audio'].read()

    # Recognize speech using Vosk
    audio_stream = io.BytesIO(audio_file)
    rec = KaldiRecognizer(model, 16000)
    transcript = ""
    while True:
        data = audio_stream.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            transcript += json.loads(result).get('text', '')

    return jsonify({'transcript': transcript})

if __name__ == '__main__':
    app.run(debug=True)
