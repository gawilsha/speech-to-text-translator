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


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print("Usage: python main.py <path_to_audio_file>", file=sys.stderr)
        sys.exit(1)

    audio_path = argv[1]

    try:
        print(f"Transcribing: {audio_path} ...")
        text = transcribe_file(audio_path)
        print("\n--- Transcript ---\n")
        print(text)

        # Save transcript to a .txt file next to the audio file
        out_path = "transcribed.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\nSaved to: {out_path}")
        # Run the async translate_text coroutine to create translated.txt
        asyncio.run(translate.translate_text())
        print("\n--- Translated Text ---\n")
        with open("translated.txt", "r", encoding="utf-8") as f:
            translated_text = f.read()
        print(translated_text)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
