# Sunbird AI — Summarise, Translate & Transcribe

## Project description

A Python web application powered by the Sunbird AI API and Sunflower LLM that accepts
either typed text or an uploaded audio file, summarises it, translates the summary into a
chosen Ugandan local language (Luganda, Runyankole, Ateso, Lugbara, or Acholi), and
synthesises the translated summary into playable speech. A Streamlit web UI surfaces every
intermediate result — transcript, summary, translated summary, and audio player.

## Architecture overview

- Input: user provides text or audio file
- Speech-to-Text (audio only): POST /tasks/stt → transcript text
- Summarise (Sunflower LLM): POST /tasks/sunflower_inference → 2-4 sentence summary
- Translate (Sunflower LLM): POST /tasks/sunflower_inference → summary in target language
- Text-to-Speech: POST /tasks/tts → audio file
- Output: transcript, summary, translated summary, audio player

## Local setup

git clone https://github.com/Kenaz79/internship-assessment.git
cd internship-assessment
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
streamlit run streamlit_app.py

## Environment variables

SUNBIRD_API_TOKEN — Your Sunbird AI API bearer token from https://api.sunbird.ai

## Usage

1. Open http://localhost:8501 in your browser
2. Choose Text or Audio input
3. Select a target language
4. Click Run pipeline
5. See transcript, summary, translated summary and audio player

## Deployed link

https://internship-assessment-zbbmi5fk2vzu4hqvf6h2vx.streamlit.app/

## Known limitations

- Audio files longer than 5 minutes are rejected
- Supported output languages: Luganda, Runyankole, Ateso, Lugbara, Acholi
- API response times may be slow depending on network speed