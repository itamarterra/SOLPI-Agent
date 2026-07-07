import pyautogui
import pytesseract
import cv2
import numpy as np
import os
from datetime import datetime

class VisionCore:
    """Motor de Visão Avançado: OCR, Template Matching e Detecção de Mudanças."""
    
    @staticmethod
    def get_screen_state():
        screenshot = pyautogui.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    @staticmethod
    def find_icon(icon_name, threshold=0.8):
        """Busca um ícone na pasta assets/icons e retorna sua posição."""
        icon_path = f"assets/icons/{icon_name}.png"
        if not os.path.exists(icon_path):
            print(f"❌ [VISION]: Ícone '{icon_name}' não encontrado em assets/icons/")
            return None
            
        screen = VisionCore.get_screen_state()
        template = cv2.imread(icon_path)
        
        res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= threshold:
            h, w = template.shape[:2]
            return {"x": max_loc[0] + w // 2, "y": max_loc[1] + h // 2, "conf": max_val}
        return None

    @staticmethod
    def extract_all_text():
        """Lê todo o texto visível na tela e suas posições."""
        screenshot = pyautogui.screenshot()
        data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT, lang='por')
        results = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 50 and data['text'][i].strip():
                results.append({
                    "text": data['text'][i],
                    "x": data['left'][i] + (data['width'][i] // 2),
                    "y": data['top'][i] + (data['height'][i] // 2)
                })
        return results

    @staticmethod
    def has_screen_changed(before_img, min_diff=1500):
        """Valida se houve mudança significativa na tela após uma ação."""
        after_img = VisionCore.get_screen_state()
        diff = cv2.absdiff(before_img, after_img)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)
        change_count = np.sum(thresh == 255)
        return change_count > min_diff, after_img
