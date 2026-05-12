from backend.sunbird_client import ALL_LANGUAGES, translate_direct


def pick_language(prompt: str, exclude: str = None) -> str:
    available = [lang for lang in ALL_LANGUAGES if lang != exclude]
    print(f"\n{prompt}")
    for i, lang in enumerate(available, 1):
        print(f"  {i}. {lang}")
    while True:
        choice = input("Enter the number or name of your choice: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(available):
                return available[idx]
        for lang in available:
            if lang.lower() == choice.lower():
                return lang
        print("  ⚠ Invalid choice. Please try again.")


def main():
    print("=" * 50)
    print("  Sunbird AI — Text Translator")
    print("=" * 50)

    source = pick_language(
        "Please choose the source language "
        f"(one of {', '.join(ALL_LANGUAGES)}):"
    )
    target = pick_language(
        "Please choose the target language "
        f"(one of {', '.join(ALL_LANGUAGES)}):",
        exclude=source,
    )

    text = input("\nEnter the text to translate:\n> ").strip()
    if not text:
        print("⚠ No text provided. Exiting.")
        return

    print("\nTranslating…")
    try:
        result = translate_direct(text, source, target)
        print(f"\n{result}")
    except Exception as e:
        print(f"\n❌ Translation failed: {e}")


if __name__ == "__main__":
    main()