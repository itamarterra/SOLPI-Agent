import pyttsx3
import speech_recognition as sr
import threading

class VoiceCore:
    """Motor de Voz do SOLPI OS: Fala e Escuta como serviço do sistema."""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self._setup_voice()

    def _setup_voice(self):
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if "brazil" in voice.name.lower() or "portuguese" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
        self.engine.setProperty('rate', 175) # Velocidade natural

    def speak(self, text, block=False):
        """Faz o agente falar. Se block for False, fala em background."""
        print(f"🤖 [VOICE]: {text}")
        if block:
            self._do_speak(text)
        else:
            threading.Thread(target=self._do_speak, args=(text,), daemon=True).start()

    def _do_speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Ouve o microfone e retorna o texto em português."""
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("🎤 [LISTENING]...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=10, phrase_time_limit=15)
            
            text = r.recognize_google(audio, language='pt-BR')
            print(f"🗣️ [USER]: {text}")
            return text
        except Exception as e:
            return None
