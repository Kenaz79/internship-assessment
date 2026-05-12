import gradio as gr
from backend.pipeline import run_pipeline
from backend.sunbird_client import LOCAL_LANGUAGES


def process(text_input, audio_file, target_language):
    try:
        transcript, summary, translated, audio_path = run_pipeline(
            text_input=text_input or None,
            audio_path=audio_file or None,
            target_language=target_language,
        )
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        return error_msg, "", "", None

    return (
        transcript if transcript is not None else "(text input — no transcription)",
        summary,
        translated,
        audio_path,
    )


with gr.Blocks(title="Sunbird AI — Summarise & Translate") as demo:

    gr.Markdown(
        """
        # 🌻 Sunbird AI — Summarise & Translate
        Powered by the **Sunflower LLM** and Sunbird AI APIs.
        Provide text or an audio file, pick a target Ugandan language, and get a
        summary, translation, and spoken audio output.
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Input")

            with gr.Tab("📝 Text"):
                text_input = gr.Textbox(
                    label="Paste or type your text",
                    lines=8,
                    placeholder="Enter text here…",
                )

            with gr.Tab("🎙️ Audio"):
                audio_input = gr.Audio(
                    label="Upload audio file (MP3, WAV, OGG, M4A — max 5 min)",
                    type="filepath",
                )

            target_lang = gr.Dropdown(
                choices=LOCAL_LANGUAGES,
                value="Luganda",
                label="Target language",
            )

            run_btn = gr.Button("Run pipeline ▶", variant="primary", size="lg")

        with gr.Column(scale=1):
            gr.Markdown("### Output")

            transcript_out = gr.Textbox(
                label="📄 Transcript (audio input only)",
                interactive=False,
                lines=4,
            )
            summary_out = gr.Textbox(
                label="📝 Summary",
                interactive=False,
                lines=4,
            )
            translated_out = gr.Textbox(
                label="🌍 Translated summary",
                interactive=False,
                lines=4,
            )
            audio_out = gr.Audio(
                label="🔊 Synthesised audio",
                interactive=False,
            )

    run_btn.click(
        fn=process,
        inputs=[text_input, audio_input, target_lang],
        outputs=[transcript_out, summary_out, translated_out, audio_out],
    )

if __name__ == "__main__":
    demo.launch()