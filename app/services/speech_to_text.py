import speech_recognition as sr

class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        with sr.Microphone() as source:
            print("\n Listening")
            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5
            )
            audio = self.recognizer.listen(
                source
            )

        try:
            text = self.recognizer.recognize_google(
                audio,
                language = "en-IN"
            )
            print("You: ", text)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError as error:
            print(
                f"Speech Recognize Error: {error}"
            )
            return ""
