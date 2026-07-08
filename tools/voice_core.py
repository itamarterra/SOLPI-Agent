import pyttsx3
import threading
import queue
import time

class VoiceCore:
    """Motor de Voz Robusto: Usa uma fila para evitar conflitos de fala."""
    def __init__(self):
        self.speech_queue = queue.Queue()
        self.stop_event = threading.Event()
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        # O motor deve ser inicializado dentro da thread que vai rodar o loop
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if "brazil" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 180)

        while not self.stop_event.is_set():
            try:
                text = self.speech_queue.get(timeout=0.5)
                if text:
                    print(f"🤖 [VOICE]: {text}")
                    engine.say(text)
                    engine.runAndWait()
                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ [VOICE ERROR]: {e}")
                time.sleep(1)

    def speak(self, text, block=False):
        """Adiciona o texto à fila de fala."""
        self.speech_queue.put(text)
        if block:
            self.speech_queue.join()

    def listen(self):
        import speech_recognition as sr
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("🎤 [OUVINDO]...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5)
            return r.recognize_google(audio, language='pt-BR')
        except: return None
