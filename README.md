# Language_Translation_App

## Overview
This application translates text from one language to another, detects the source language, converts speech to text, and plays back translated text using text-to-speech functionality.

## Features
- Text Translation
- Language Detection
- Speech-to-Text
- Text-to-Speech

## Setup Instructions

### Prerequisites
- Python 3.8 or later
- Pip (Python package installer)
- A Vosk model for speech recognition

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/language_translation_app.git
    cd language_translation_app
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Download the Vosk model and place it in the `model` directory:
    - [Vosk Models](https://alphacephei.com/vosk/models)

5. Run the application:
    ```bash
    python app.py
    ```

6. Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
- Use the text input to enter the text you want to translate and specify the target language code.
- Use the "Speak" functionality to convert text to speech.
- Use the "Speech to Text" functionality to upload an audio file and convert it to text.
