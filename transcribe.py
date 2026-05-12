import os
from backend.sunbird_client import ALL_LANGUAGES, transcribe
from backend.pipeline import get_audio_duration_seconds, MAX_AUDIO_SECONDS


def pick_language(prompt: str) -> str:
    print(f"\n{prompt}")
    for i, lang in enumerate(ALL_LANGUAGES, 1):
        print(f"  {i}. {lang}")
    while True:
        choice = input("Enter the number or name of your choice: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(ALL_LANGUAGES):
                return ALL_LANGUAGES[idx]
        for lang in ALL_LANGUAGES:
            if lang.lower() == choice.lower():
                return lang
        print("  ⚠ Invalid choice. Please try again.")


def main():
    print("=" * 50)
    print("  Sunbird AI — Audio Transcription")
    print("=" * 50)

    while True:
        audio_path = input(
            "\nPlease provide the path to the audio file "
            "(audio length must be less than 5 minutes):\n> "
        ).strip()

        if not os.path.isfile(audio_path):
            print(f"  ⚠ File not found: {audio_path!r}. Please try again.")
            continue

        try:
            duration = get_audio_duration_seconds(audio_path)
        except Exception as e:
            print(f"  ⚠ Could not read audio file: {e}")
            continue

        if duration > MAX_AUDIO_SECONDS:
            print(
                f"  ⚠ Audio is {duration:.0f} s ({duration/60:.1f} min) — "
                "exceeds the 5-minute limit. Please provide a shorter file."
            )
            continue

        print(f"  ✓ File accepted ({duration:.0f} s)")
        break

    language = pick_language(
        "Please choose the language the audio is in "
        f"(one of {', '.join(ALL_LANGUAGES)}):"
    )

    print("\nTranscribing… (this may take a moment)")
    try:
        text = transcribe(audio_path)
        print(f"\nAudio transcription text in {language}:")
        print(text)
    except Exception as e:
        print(f"\n❌ Transcription failed: {e}")


if __name__ == "__main__":
    main()