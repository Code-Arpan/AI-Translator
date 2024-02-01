from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import openai
import speech_recognition as sr

app = Flask(__name__)

# Set your OpenAI API key here
api_key = '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'
openai.api_key = api_key

# Language code mapping for gTTS
language_codes = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese (Simplified)': 'zh-cn',
    'Hindi': 'hi',
    'Arabic': 'ar',
    'Russian': 'ru',
    'Japanese': 'ja',
    'Portuguese': 'pt',
    'Bengali': 'bn',
    'Urdu': 'ur',
    'Turkish': 'tr',
    'Vietnamese': 'vi',
    'Korean': 'ko',
    'Italian': 'it',
    'Tamil': 'ta',
    'Marathi': 'mr',
    'Telugu': 'te',
    'Czech': 'cs',
    'Dutch': 'nl',
}

@app.route('/')
def index():
    return render_template('index.html', languages=language_codes.keys())

@app.route('/translate', methods=['POST'])
def translate():
    source_text = request.form['source_text']
    source_language = request.form['source_language']
    target_language = request.form['target_language']

    source_language_code = language_codes.get(source_language, 'en')
    target_language_code = language_codes.get(target_language, 'en')

    prompt = f"Translate the following text from {source_language} to {target_language}:\n\n{source_text}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100
    )

    translated_text = response['choices'][0]['text'].strip()

    # Text-to-Speech using gTTS
    tts = gTTS(translated_text, lang=target_language_code)
    tts.save("static/translated_audio.mp3")

    return render_template('index.html', source_text=source_text, source_language=source_language,
                           translated_text=translated_text, target_language=target_language,
                           languages=language_codes.keys())

@app.route('/speech_input', methods=['POST'])
def speech_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Speak something in the source language...")
        audio = recognizer.listen(source)

    try:
        source_text = recognizer.recognize_google(audio, language='en')  # Assuming English as the source language
        return jsonify({'source_text': source_text})
    except sr.UnknownValueError:
        return jsonify({'error': 'Speech not recognized'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
