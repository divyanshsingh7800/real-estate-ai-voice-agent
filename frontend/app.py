import streamlit as st
import requests
import asyncio
import edge_tts
import hashlib

from streamlit_mic_recorder import mic_recorder


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Real Estate AI Voice Agent",
    page_icon="🏠",
    layout="centered"
)


# ==========================================
# API
# ==========================================

API_URL = "http://127.0.0.1:8000/chat"


# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "customer_data" not in st.session_state:
    st.session_state.customer_data = {}

if "lead_id" not in st.session_state:
    st.session_state.lead_id = None

if "audio_response" not in st.session_state:
    st.session_state.audio_response = None

# Prevent duplicate processing of the same browser recording.
if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


# ==========================================
# SEND MESSAGE TO FASTAPI
# ==========================================

def send_to_agent(text):

    try:

        response = requests.post(
            API_URL,
            json={"message": text},
            timeout=60
        )

        if response.status_code == 200:
            return response.json()

        st.error(
            f"FastAPI Error: {response.status_code}"
        )

        return None

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ FastAPI server is not running."
        )

        return None

    except Exception as error:

        st.error(
            f"Error: {error}"
        )

        return None


# ==========================================
# TEXT TO SPEECH
# ==========================================

async def generate_tts(text):

    communicate = edge_tts.Communicate(
        text=text,
        voice="hi-IN-SwaraNeural",
        rate="+0%",
        volume="+0%"
    )

    audio_data = b""

    async for chunk in communicate.stream():

        if chunk["type"] == "audio":
            audio_data += chunk["data"]

    return audio_data


def speak_response(text):

    try:

        audio_bytes = asyncio.run(
            generate_tts(text)
        )

        st.session_state.audio_response = audio_bytes

    except Exception as error:

        st.warning(
            f"TTS Error: {error}"
        )


# ==========================================
# PROCESS MESSAGE
# ==========================================

def process_message(text):

    if not text:
        return

    # ------------------------------
    # USER MESSAGE
    # ------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": text
    })


    # ------------------------------
    # SEND TO FASTAPI
    # ------------------------------

    result = send_to_agent(text)


    if result:

        ai_response = result.get(
            "response",
            ""
        )

        customer_data = result.get(
            "customer_data",
            {}
        )

        lead_id = result.get(
            "lead_id"
        )


        # ------------------------------
        # SAVE CUSTOMER DATA
        # ------------------------------

        st.session_state.customer_data = (
            customer_data
        )


        # ------------------------------
        # SAVE LEAD ID
        # ------------------------------

        st.session_state.lead_id = lead_id


        # ------------------------------
        # SAVE AI RESPONSE
        # ------------------------------

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response
        })


        # ------------------------------
        # GENERATE AI VOICE
        # ------------------------------

        speak_response(
            ai_response
        )


# ==========================================
# HEADER
# ==========================================

st.title(
    "🏠 Real Estate AI Voice Agent"
)

st.write(
    "AI-powered property recommendation "
    "and lead qualification system."
)


# ==========================================
# CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ==========================================
# VOICE AGENT
# ==========================================

st.subheader("🎤 Talk to AI Agent")

# A new recorder key is created after every successful message.
# This makes the microphone available again for the next turn.
recorder_key = f"voice_recorder_{len(st.session_state.messages)}"

audio = mic_recorder(
    start_prompt="🎤 Start Speaking",
    stop_prompt="⏹️ Stop Recording",
    just_once=True,
    use_container_width=True,
    format="wav",
    key=recorder_key
)

# ==========================================
# PROCESS VOICE
# ==========================================

if audio and audio.get("bytes"):

    audio_bytes = audio["bytes"]

    # Prevent the same browser recording from being processed twice.
    current_audio_hash = hashlib.md5(audio_bytes).hexdigest()

    if current_audio_hash != st.session_state.last_audio_hash:

        st.session_state.last_audio_hash = current_audio_hash

        st.audio(
            audio_bytes,
            format="audio/wav"
        )

        st.info("🎤 Voice recorded. Processing...")

        # ------------------------------
        # SAVE AUDIO
        # ------------------------------

        audio_path = "user_voice.wav"

        with open(audio_path, "wb") as file:
            file.write(audio_bytes)

        # ------------------------------
        # SPEECH TO TEXT
        # ------------------------------

        text = ""

        try:
            import speech_recognition as sr

            recognizer = sr.Recognizer()

            with sr.AudioFile(audio_path) as source:
                recorded_audio = recognizer.record(source)

            text = recognizer.recognize_google(
                recorded_audio,
                language="en-IN"
            )

            st.write(f"👤 **You:** {text}")

        except sr.UnknownValueError:
            st.error("❌ Could not understand your voice.")

        except sr.RequestError as error:
            st.error(f"Speech Recognition Error: {error}")

        except Exception as error:
            st.error(f"Voice Processing Error: {error}")

        # ------------------------------
        # SEND TO AGENT
        # ------------------------------

        if text:
            process_message(text)

            # Rerun creates a fresh microphone component
            # because recorder_key changes with message count.
            st.rerun()


# ==========================================
# AI VOICE RESPONSE
# ==========================================

if st.session_state.audio_response:

    st.subheader(
        "🔊 AI Voice Response"
    )

    st.audio(
        st.session_state.audio_response,
        format="audio/mp3",
        autoplay=True
    )


# ==========================================
# TEXT INPUT
# ==========================================

st.divider()

st.subheader(
    "💬 Or type your message"
)


text_message = st.chat_input(
    "Enter your property requirement..."
)


if text_message:

    process_message(
        text_message
    )

    st.rerun()


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header(
        "📋 Customer Information"
    )

    data = st.session_state.customer_data


    st.write(
        "**Name:**",
        data.get("name")
    )

    st.write(
        "**Phone:**",
        data.get("phone")
    )

    st.write(
        "**Location:**",
        data.get("location")
    )

    st.write(
        "**Property Type:**",
        data.get("property_type")
    )

    st.write(
        "**BHK:**",
        data.get("bhk")
    )

    st.write(
        "**Budget:**",
        data.get("budget_max")
    )

    st.write(
        "**Timeline:**",
        data.get("timeline")
    )

    st.write(
        "**Purpose:**",
        data.get("purpose")
    )

    st.write(
        "**Selected Property:**",
        data.get("selected_property")
    )


    if st.session_state.lead_id:

        st.success(
            f"Lead ID: "
            f"{st.session_state.lead_id}"
        )


# ==========================================
# CLEAR CONVERSATION
# ==========================================

if st.button(
    "Clear Conversation"
):

    st.session_state.messages = []

    st.session_state.customer_data = {}

    st.session_state.lead_id = None

    st.session_state.audio_response = None

    st.session_state.last_audio_hash = None

    st.rerun()