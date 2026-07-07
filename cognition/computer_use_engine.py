import time
import pyautogui
from tools.vision_core import VisionCore
from tools.gui_tools import GUITools

class ComputerUseEngine:
    """
    O Motor de Uso de Computador do SOLPI OS.
    Gerencia interações físicas e valida resultados visuais.
    """
    def __init__(self, memory):
        self.memory = memory
        self.vision = VisionCore()
        self.gui = GUITools()

    def perform_action(self, action_type, params):
        """Executa uma ação e verifica se a tela mudou como esperado."""
        print(f"🖱️ [CUE]: Executando {action_type} com validação visual...")
        
        # 1. Salva o estado visual ANTES da ação
        before_img = self.vision.get_screen_state()
        
        # 2. Executa a ação
        result = self._dispatch(action_type, params)
        
        # 3. Espera o sistema reagir
        time.sleep(1)
        
        # 4. Verifica o estado DEPOIS da ação
        after_img = self.vision.get_screen_state()
        
        changed = self.vision.has_screen_changed(before_img, after_img)
        
        if not changed:
            print("⚠️ [CUE]: A tela não mudou após a ação. Verificando possível falha...")
            return {"status": "warning", "msg": "Ação executada, mas sem resposta visual.", "result": result}
            
        return {"status": "success", "result": result}

    def _dispatch(self, action, p):
        if action == "click":
            if "text" in p:
                pos = self.gui.find_text_on_screen(p["text"])
                if pos: return self.gui.click(pos["x"], pos["y"])
            return self.gui.click(p["x"], p["y"])
            
        elif action == "type":
            return self.gui.type_text(p["text"])
            
        elif action == "open_app":
            import subprocess
            subprocess.run(f"start {p['name']}", shell=True)
            return f"Iniciando {p['name']}..."
            
        return "Ação desconhecida."
