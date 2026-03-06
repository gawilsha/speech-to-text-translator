from googletrans import Translator
import asyncio

async def translate_text():
    translator = Translator()

    f = open("transcribed.txt", "r", encoding="utf-8")
    text = f.read()

    # translate the text to new language
    translated = await translator.translate(text, src="en", dest="fr")

    # save the translated text to a new file
    with open("translated.txt", "w", encoding="utf-8") as f:
        f.write(translated.text)

if __name__ == "__main__":
    asyncio.run(translate_text())