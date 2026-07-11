import numpy as np

class Tensor:
    """
    PACOTE 0080: NEURAL TENSOR CORE v80.0 (Singularity Engine)
    Base para o grafo computacional nativo do SOLPI-OS.
    """
    def __init__(self, data, requires_grad=False):
        self.data = np.array(data, dtype=np.float32)
        self.requires_grad = requires_grad
        self.grad = None
        self._prev = set()
        self._op = ""

    def __repr__(self):
        return f"SOLPI-Tensor(data={self.data}, grad={self.grad})"

    def add(self, other):
        other = other if isinstance(other, Tensor) else Tensor(other)
        out = Tensor(self.data + other.data, requires_grad=(self.requires_grad or other.requires_grad))
        out._prev = {self, other}
        out._op = "+"
        return out

    def matmul(self, other):
        # Garante que other seja um array numpy para a operação @
        other_data = other.data if isinstance(other, Tensor) else np.array(other)
        out = Tensor(self.data @ other_data, requires_grad=(self.requires_grad or (isinstance(other, Tensor) and other.requires_grad)))
        out._prev = {self} if not isinstance(other, Tensor) else {self, other}
        out._op = "@"
        return out

class NeuralVM:
    """
    VIRTUAL MACHINE v80.2 (Singularity Execution)
    Executa o Bytecode gerado pelo compilador IR do SOLPI.
    Interface direta com o Tensor Core e Predictor.
    """
    def __init__(self, brain):
        self.brain = brain
        self.registers = {}

    def execute_bytecode(self, bytecode):
        """
        Interpreta e executa a Instruction Set Architecture (ISA).
        """
        self.brain.kernel.log_event("NEURAL_VM", f"Iniciando execução de {len(bytecode)} instruções...")
        
        pc = 0 # Program Counter
        while pc < len(bytecode):
            op = bytecode[pc]
            
            if op == 0x01: # LOAD
                reg = bytecode[pc+1]
                # Simulação de carga de dados do sistema
                self.registers[reg] = [0.85, 0.92, 0.45, 0.10, 0.05, 0.30]
                pc += 2
            elif op == 0x05: # PREDICT
                reg = bytecode[pc+1]
                data = self.registers[reg]
                # Invoca o motor preditivo usando tensores
                result = self.brain.predictor.analyze_trend([data])
                self.registers["ACC"] = result # Acumulador
                pc += 2
            elif op == 0x04: # STORE
                reg = bytecode[pc+1]
                self.registers[reg] = self.registers.get("ACC")
                pc += 2
            elif op == 0xFF: # HALT
                break
            else:
                pc += 1
                
        self.brain.kernel.log_event("NEURAL_VM", "Execução concluída com sucesso.")
        return self.registers.get("STORE_RESULT", self.registers.get("ACC", "OK"))
