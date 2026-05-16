import streamlit as st
from backend.pipeline import run_pipeline
from backend.sunbird_client import LOCAL_LANGUAGES

st.set_page_config(page_title="Sunbird AI", page_icon="🌻")

st.title("🌻 Sunbird AI — Summarise & Translate")
st.markdown("Powered by **Sunflower LLM** and Sunbird AI APIs.")

# Input section
st.subheader("Input")
input_type = st.radio("Choose input type:", ["📝 Text", "🎙️ Audio"])

text_input = None
audio_input = None

if input_type == "📝 Text":
    text_input = st.text_area("Paste or type your text here:", height=200)
else:
    audio_input = st.file_uploader(
        "Upload audio file (MP3, WAV, OGG — max 5 min)",
        type=["mp3", "wav", "ogg", "m4a"]
    )

target_lang = st.selectbox("Target language:", LOCAL_LANGUAGES)

if st.button("▶ Run pipeline", type="primary"):
    if not text_input and not audio_input:
        st.error("Please provide text or an audio file.")
    else:
        # Save uploaded audio to temp file if needed
        audio_path = None
        if audio_input:
            import tempfile, os
            suffix = os.path.splitext(audio_input.name)[1]
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tmp.write(audio_input.read())
            tmp.close()
            audio_path = tmp.name

        with st.spinner("Running pipeline... please wait"):
            try:
                transcript, summary, translated, local_audio = run_pipeline(
                    text_input=text_input or None,
                    audio_path=audio_path or None,
                    target_language=target_lang,
                )

                st.subheader("Output")

                if transcript:
                    st.markdown("**📄 Transcript:**")
                    st.info(transcript)

                st.markdown("**📝 Summary:**")
                st.success(summary)

                st.markdown("**🌍 Translated Summary:**")
                st.success(translated)

                st.markdown("**🔊 Synthesised Audio:**")
                with open(local_audio, "rb") as f:
                    st.audio(f.read(), format="audio/wav")

            except Exception as e:
                st.error(f"❌ Error: {e}")