import streamlit as st
from deep_translator import GoogleTranslator
from deep_translator.constants import GOOGLE_LANGUAGES_TO_CODES
from gtts import gTTS
import base64


st.set_page_config(page_title="Voice Translator", page_icon="🌍")

st.title("🌍 Voice Language Translation Tool")
st.write("Type text and translate easily (voice input removed for stability)")


languages = list(GOOGLE_LANGUAGES_TO_CODES.keys())


text = st.text_area("✏️ Enter text here")


source_lang = st.selectbox("🔤 Source Language", languages)
target_lang = st.selectbox("🔤 Target Language", languages)


if st.button("Translate 🔄"):
    if text.strip() == "":
        st.warning("Please enter text!")
    else:
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)

            st.success("Translated Text:")
            st.text_area("Output", result, height=150)

            # Save for speech
            st.session_state["translated_text"] = result

        except Exception as e:
            st.error(f"Error: {e}")


def speak_text(text, lang="en"):
    tts = gTTS(text=text, lang=lang)
    file = "voice.mp3"
    tts.save(file)

    audio = open(file, "rb").read()
    b64 = base64.b64encode(audio).decode()

    st.markdown(
        f"""
        <audio controls autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )

if "translated_text" in st.session_state:
    if st.button("🔊 Speak Translation"):
        speak_text(st.session_state["translated_text"], "en")


st.markdown("---")
st.caption("Made for CodeAlpha Internship Task 1 🚀")