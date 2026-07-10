class SOLPIModelRegistry:
    """
    PACOTE 8000: MODEL REGISTRY v1.0
    Abstrai o cérebro dos modelos específicos (Llama, Qwen, DeepSeek, etc).
    Permite troca a quente de modelos sem alterar a lógica de negócio.
    """
    def __init__(self, brain):
        self.brain = brain
        self.models = {
            "native": self.brain.native_core, # Nosso motor NumPy
            "qwen": "api://qwen-2.5-7b",
            "llama": "api://llama-3.1-8b",
            "deepseek": "api://deepseek-coder"
        }
        self.active_model_name = "native"

    def get_model(self, name=None):
        name = name or self.active_model_name
        return self.models.get(name, self.models["native"])

    def switch_model(self, name):
        if name in self.models:
            self.active_model_name = name
            self.brain.kernel.log_event("REGISTRY", f"🧠 Modelo trocado para: {name}")
            return True
        return False
