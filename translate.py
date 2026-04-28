from googletrans import Translator
import asyncio


async def translate_text(text: str, dest: str = "fr", src: str = "auto") -> str:
    translator = Translator()
    translated = await translator.translate(text, src=src, dest=dest)
    return translated.text


if __name__ == "__main__":
    with open("transcribed.txt", "r", encoding="utf-8") as f:
        transcript_text = f.read()

    translated_text = asyncio.run(translate_text(transcript_text))
    with open("translated.txt", "w", encoding="utf-8") as f:
        f.write(translated_text)
