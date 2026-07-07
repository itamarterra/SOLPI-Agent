import pyautogui
import pytesseract
import os
from datetime import datetime

class GUITools:
    """Ferramentas de Automação de Desktop e Visão."""
    
    @staticmethod
    def capture_screen():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"memory/screenshots/view_{timestamp}.png"
        os.makedirs("memory/screenshots", exist_ok=True)
        pyautogui.screenshot(path)
        return path

    @staticmethod
    def find_text_on_screen(text):
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT, lang='por')
        for i in range(len(data['text'])):
            if text.lower() in data['text'][i].lower():
                return {
                    "x": data['left'][i] + (data['width'][i] // 2),
                    "y": data['top'][i] + (data['height'][i] // 2)
                }
        return None

    @staticmethod
    def click(x, y):
        pyautogui.click(x, y)
        return f"Clique realizado em {x}, {y}"

    @staticmethod
    def type_text(text):
        pyautogui.write(text, interval=0.05)
        return "Texto digitado."
