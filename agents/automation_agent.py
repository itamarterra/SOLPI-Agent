import pyautogui
import pytesseract
import time
import os
import pygetwindow as gw
from agents.base_agent import BaseAgent
from datetime import datetime

class AutomationAgent(BaseAgent):
    """
    O Agente de Mãos: Especialista em interagir com QUALQUER interface de usuário (UI).
    Usa Visão Computacional (OCR) para não depender de coordenadas fixas.
    """
    def register_tools(self):
        if self.registry:
            self.registry.register("AutomationAgent", "click_text", "Localizar texto na tela e clicar nele")
            self.registry.register("AutomationAgent", "type_text", "Digitar texto na janela ativa")
            self.registry.register("AutomationAgent", "press_key", "Pressionar uma tecla ou atalho")
            self.registry.register("AutomationAgent", "screenshot", "Capturar imagem da tela para análise")

    def execute(self, task_description):
        print(f"🖱️ [AUTOMATION AGENT]: Agindo -> {task_description}")
        task_lower = task_description.lower()
        
        if "clique" in task_lower:
            target = task_lower.replace("clique no texto", "").replace("clique em", "").replace("clique", "").strip()
            return self._click_on_text(target)
            
        elif "digite" in task_lower:
            content = task_description.split("digite")[-1].strip()
            return self._type_text(content)

        elif "pressione" in task_lower or "aperte" in task_lower:
            key = task_lower.split()[-1].strip()
            return self._press_key(key)

        elif "print" in task_lower or "veja" in task_lower:
            return self._take_view_screenshot()

        return f"AutomationAgent: Tarefa '{task_description}' requer instruções de UI mais específicas."

    def _click_on_text(self, text):
        print(f"👁️ [VISÃO]: Escaneando tela em busca de '{text}'...")
        try:
            screenshot = pyautogui.screenshot()
            data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT, lang='por')
            
            for i in range(len(data['text'])):
                if text.lower() in data['text'][i].lower():
                    x = data['left'][i] + (data['width'][i] // 2)
                    y = data['top'][i] + (data['height'][i] // 2)
                    pyautogui.click(x, y)
                    self.log_activity(f"Clicou no texto '{text}' em {x},{y}")
                    return f"✅ Clique realizado em '{data['text'][i]}'."
            
            return f"🔍 Texto '{text}' não encontrado na tela atual."
        except Exception as e:
            return f"❌ Falha na visão: {str(e)}"

    def _type_text(self, text):
        try:
            pyautogui.write(text, interval=0.05)
            self.log_activity(f"Digitou: {text}")
            return f"✅ Texto digitado."
        except Exception as e:
            return str(e)

    def _press_key(self, key):
        try:
            pyautogui.press(key)
            self.log_activity(f"Pressionou tecla: {key}")
            return f"✅ Tecla {key} pressionada."
        except Exception as e:
            return str(e)

    def _take_view_screenshot(self):
        os.makedirs("memory/views", exist_ok=True)
        path = f"memory/views/view_{datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot(path)
        return f"📸 Tela capturada em {path}"
