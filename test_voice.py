from app.agent.agent import RealEstateAgent
from app.services.speech_to_text import SpeechToText
from app.services.text_to_speech import TextToSpeech


def main():

    print("==============================")
    print(" Real Estate Voice Agent ")
    print("==============================")

    stt = SpeechToText()
    tts = TextToSpeech()
    agent = RealEstateAgent()

    # Initial greeting
    tts.speak(
        "Hello! Welcome to our real estate service. "
        "How can I help you find your property?"
    )

    while True:

        # Listen to customer
        text = stt.listen()

        if not text:
            continue

        print("Customer:", text)

        # Exit
        if text.lower().strip() in [
            "exit",
            "quit",
            "stop",
            "bye"
        ]:
            tts.speak(
                "Thank you for your time. Have a great day!"
            )
            break

        # Process message
        result = agent.process_message(text)

        # AI response
        response = result.get("response")

        # Speak response
        if response:
            tts.speak(response)

        # Lead saved
        if result.get("lead_id"):

            print("\n==============================")
            print(" Lead Successfully Saved")
            print("==============================")

            print("Lead ID:", result["lead_id"])

            tts.speak(
                "Your lead has been successfully registered. "
                "Our team will contact you shortly. Thank you!"
            )

            break


if __name__ == "__main__":
    main()