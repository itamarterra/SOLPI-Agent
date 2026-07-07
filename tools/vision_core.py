import pyautogui
import pytesseract
import cv2
import numpy as np
import os
from datetime import datetime

class VisionCore:
    """Motor de Visão Avançado com suporte a reconhecimento de objetos."""
    
    @staticmethod
    def get_screen_state():
        """Captura o estado visual atual da tela."""
        screenshot = pyautogui.screenshot()
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return img

    @staticmethod
    def find_element_by_image(template_path, threshold=0.8):
        """Procura um ícone ou botão na tela usando uma imagem de referência."""
        if not os.path.exists(template_path):
            return None
            
        screen = VisionCore.get_screen_state()
        template = cv2.imread(template_path)
        
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            # Retorna o centro do elemento encontrado
            h, w = template.shape[:2]
            return {
                "x": max_loc[0] + w // 2,
                "y": max_loc[1] + h // 2,
                "confidence": max_val
            }
        return None

    @staticmethod
    def read_text_at_area(region=None):
        """Lê texto em uma região específica (x, y, w, h)."""
        screenshot = pyautogui.screenshot(region=region) if region else pyautogui.screenshot()
        return pytesseract.image_to_string(screenshot, lang='por').strip()

    @staticmethod
    def has_screen_changed(last_state_img, current_state_img, min_diff=1000):
        """Compara duas imagens para saber se a ação causou mudança na tela."""
        diff = cv2.absdiff(last_state_img, current_state_img)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        change_count = np.sum(thresh == 255)
        return change_count > min_diff
