import os
import sys

import assemblyai as aai
import asyncio
import translate


def get_api_key() -> str:
    # Read the API key from the ASSEMBLYAI_API_KEY environment variable
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing ASSEMBLYAI_API_KEY environment variable.\n"
            "Sign up at https://www.assemblyai.com, create an API key,\n"
            "then set it in your environment, e.g. on PowerShell:\n"
            '  $env:ASSEMBLYAI_API_KEY = "your_api_key_here"'
        )
    return api_key


def transcribe_file(audio_path: str) -> str:
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    aai.settings.api_key = get_api_key()

    # Tell AssemblyAI which speech model(s) to use
    config = aai.TranscriptionConfig(
        speech_models=["universal-3-pro", "universal-2"],
        # or, if you prefer: speech_models=["universal-2"],
    )

    # Pass the config into the Transcriber so speech_models is sent
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return transcript.text or ""


def process_audio(audio_path: str, target_language: str = "fr") -> tuple[str, str]:
    text = transcribe_file(audio_path)
    translated_text = asyncio.run(translate.translate_text(text, dest=target_language))

    with open("transcribed.txt", "w", encoding="utf-8") as f:
        f.write(text)
    with open("translated.txt", "w", encoding="utf-8") as f:
        f.write(translated_text)

    return text, translated_text


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print(
            "Usage: python main.py <path_to_audio_file> [target_language_code]",
            file=sys.stderr,
        )
        sys.exit(1)

    audio_path = argv[1]
    target_language = argv[2] if len(argv) > 2 else "fr"

    try:
        print(f"Transcribing: {audio_path} ...")
        text, translated_text = process_audio(audio_path, target_language)
        print("\n--- Transcript ---\n")
        print(text)
        print("\n--- Translated Text ---\n")
        print(translated_text)
        print("\nSaved to: transcribed.txt and translated.txt")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
