from app.services.text_to_speech import TextToSpeech


tts = TextToSpeech()

tts.speak(
    "Namaste! Aapka swagat hai. "
    "Aapko kis location mein property chahiye?"
)

tts.speak(
    "Aapka maximum budget kitna hai?"
)

tts.speak(
    "Aap property self use ke liye le rahe hain ya investment ke liye?"
)