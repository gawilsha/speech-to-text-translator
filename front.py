import streamlit as st
import main
from pathlib import Path

st.title("Speech to Text Translator")
st.write("Upload an audio file and we'll transcribe it and translate it to your desired language.")

audio_file = st.file_uploader(
    "Upload an audio file",
    type=["mp3", "wav", "m4a", "flac", "ogg", "aac"]  # only audio extensions
)

language = st.selectbox(
    "Translate to:",
    ["en", "fr", "es", "de", "it", "pt", "ru", "zh-tw", "ja", "ko", "ar", "hi", "bn", "da", "nl", "el", "pl", "ro", "sv", "tr", "uk", "vi"]
)

if audio_file is not None:
    st.audio(audio_file)  # optional preview player
    st.success(f"Uploaded {audio_file.name}. Ready to transcribe.")
    if st.button("Transcribe"):
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        audio_path = upload_dir / audio_file.name

        with open(audio_path, "wb") as f:
            f.write(audio_file.getbuffer())

        with st.spinner("Transcribing and translating..."):
            transcript_text, translated_text = main.process_audio(str(audio_path), language)

        st.subheader("Transcript")
        st.write(transcript_text)
        st.subheader(f"Translation ({language})")
        st.write(translated_text)
else:
    st.info("Please upload an audio file to continue.")