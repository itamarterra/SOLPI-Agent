class Reflection:
    """O Analista de Resultados do SOLPI OS."""
    
    def __init__(self, memory, voice):
        self.memory = memory
        self.voice = voice

    def evaluate_task(self, objective, result):
        """Reflete se a tarefa foi concluída ou se precisa de correção."""
        print(f"🧐 [REFLECTION]: Auditando resultado...")
        
        is_success = "error" not in str(result).lower() and "failure" not in str(result).lower()
        
        if not is_success:
            self.voice.speak("Detectei uma anomalia na execução. Iniciando diagnóstico.")
            return {"status": "retry", "reason": "Erro técnico detectado na saída."}

        return {"status": "done", "feedback": "Tarefa validada."}
