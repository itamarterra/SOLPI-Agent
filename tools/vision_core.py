import pyautogui
import pytesseract
import cv2 # OpenCV
import numpy as np

class VisionCore:
    """Motor de Visão do SOLPI OS."""
    
    @staticmethod
    def get_screen_text():
        """Lê todo o texto da tela via OCR."""
        screenshot = pyautogui.screenshot()
        # Converte para escala de cinza para melhor OCR via OpenCV
        cv_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
        return pytesseract.image_to_string(cv_img, lang='por')

    @staticmethod
    def find_and_click(element_name):
        """Usa Template Matching para achar ícones ou botões."""
        # Implementação de busca por imagem aqui
        print(f"👁️ [VISION]: Procurando visualmente por '{element_name}'...")
        return False
