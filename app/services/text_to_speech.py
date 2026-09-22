import asyncio
import os
import edge_tts
import pygame


class TextToSpeech:

    def __init__(self):

        # Indian Hindi female voice
        self.voice = "hi-IN-SwaraNeural"

        # Temporary audio file
        self.audio_file = "temp_response.mp3"

        # Initialize pygame audio
        pygame.mixer.init()

    async def _generate_audio(self, text):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate="+0%",
            volume="+0%"
        )

        await communicate.save(self.audio_file)

    def speak(self, text):

        if not text:
            return

        print("AI:", text)

        try:

            # Generate Hindi speech
            asyncio.run(self._generate_audio(text))

            # Play audio
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()

            # Wait until audio finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

        except Exception as error:

            print("TTS Error:", error)

        finally:

            # Delete temporary audio
            if os.path.exists(self.audio_file):

                try:
                    os.remove(self.audio_file)

                except PermissionError:
                    pass