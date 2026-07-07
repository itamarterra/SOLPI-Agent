class DecisionMaker:
    """
    O Tomador de Decisão do SOLPI-AIOS.
    Avalia as opções do Reasoner e escolhe a ação com melhor custo-benefício.
    """
    def __init__(self, memory):
        self.memory = memory

    def decide(self, options):
        """
        Analisa uma lista de opções e escolhe a vencedora.
        Expects: [{'name': '...', 'risk': '...', 'score': 0.8}]
        """
        print("🤔 [DECISION]: Avaliando rotas de execução...")
        
        if not options:
            return None

        # Ordena por score (descendente) e risco (ascendente)
        sorted_options = sorted(
            options, 
            key=lambda x: (x.get('score', 0), -1 if x.get('risk') == 'Baixo' else 0), 
            reverse=True
        )
        
        choice = sorted_options[0]
        print(f"🎯 [DECISION]: Escolha final -> {choice['name']}")
        
        return choice
