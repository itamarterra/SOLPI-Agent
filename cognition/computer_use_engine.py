import time
import pyautogui
from tools.vision_core import VisionCore
from tools.gui_tools import GUITools

class ComputerUseEngine:
    """
    O Braço Motor do SOLPI OS: Executa ações e recupera falhas visuais.
    """
    def __init__(self, memory, voice):
        self.memory = memory
        self.vision = VisionCore()
        self.gui = GUITools()
        self.voice = voice

    def execute_with_recovery(self, action_type, params, max_retries=2):
        """Executa uma ação com validação visual e tentativas de recuperação."""
        for attempt in range(max_retries + 1):
            if attempt > 0:
                self.voice.speak(f"Ação falhou. Tentando recuperação, tentativa {attempt}...")
                time.sleep(2) # Espera extra na recuperação

            # 1. Foto 'Antes'
            before_img = self.vision.get_screen_state()
            
            # 2. Age
            print(f"🖱️ [CUE]: Tentativa {attempt + 1} para {action_type}")
            result = self._dispatch(action_type, params)
            
            # 3. Valida
            time.sleep(1.5)
            changed, _ = self.vision.has_screen_changed(before_img)
            
            if changed or action_type == "type": # Digitação nem sempre muda o visual bruscamente
                return {"status": "success", "result": result}
        
        return {"status": "failure", "error": "A tela não reagiu à ação."}

    def _dispatch(self, action, p):
        if action == "click":
            # Primeiro tenta por ícone se especificado
            if "icon" in p:
                pos = self.vision.find_icon(p["icon"])
                if pos: return self.gui.click(pos["x"], pos["y"])
            
            # Depois tenta por texto
            if "text" in p:
                elements = self.vision.extract_all_text()
                for el in elements:
                    if p["text"].lower() in el["text"].lower():
                        return self.gui.click(el["x"], el["y"])
            
            # Fallback para coordenadas
            if "x" in p and "y" in p:
                return self.gui.click(p["x"], p["y"])
                
        elif action == "type":
            return self.gui.type_text(p["text"])
            
        return "Ação não suportada pelo driver CUE."
