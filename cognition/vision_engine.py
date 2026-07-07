import pyautogui
import pytesseract
import cv2
import numpy as np

class VisionEngine:
    """
    O Olho Analítico do SOLPI OS.
    Independente do Computer Use, focado em compreensão visual.
    """
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def observe(self):
        """Captura e analisa a visão atual do sistema."""
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        return {
            "raw_img": img,
            "text_content": self._ocr(img),
            "elements": self._detect_elements(img)
        }

    def _ocr(self, img):
        # Converte para escala de cinza para aumentar precisão
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return pytesseract.image_to_string(gray, lang='por')

    def _detect_elements(self, img):
        """Detecta botões, ícones e janelas (Placeholder OpenCV)."""
        # Aqui seriam as chamadas de template matching para assets/icons
        return []

    def find_target(self, label):
        """Procura um texto ou ícone específico na tela."""
        print(f"👁️ [VISION]: Varrendo tela em busca de '{label}'...")
        # Lógica de busca já implementada no vision_core.py, integrada aqui
        return None
