import numpy as np
import time
from intelligence.layers.isa import SOLPI_ISA

class SOLPINeuralVM:
    """
    PACOTE 3020: AI VIRTUAL MACHINE v1.0
    Executa o Bytecode Neural do SOLPI-OS.
    Desacopla a arquitetura do modelo da execução física.
    """
    def __init__(self, brain):
        self.brain = brain
        self.registers = {} # Cache de Tensores Ativos
        self.program_counter = 0
        self.profiler_data = []

    def execute(self, bytecode):
        """Loop de execução da VM (Fetch-Decode-Execute)."""
        self.program_counter = 0
        self.brain.kernel.log_event("NEURAL_VM", "Iniciando execução de bytecode...")
        
        while self.program_counter < len(bytecode):
            instr, args = bytecode[self.program_counter]
            start_t = time.time()
            
            # Decode & Execute
            result = self._dispatch(instr, args)
            
            # Profiling
            self.profiler_data.append({
                "instr": instr,
                "duration": time.time() - start_t
            })
            
            self.program_counter += 1
        
        return result

    def _dispatch(self, instr, args):
        """Despacha a instrução para o Kernel matemático correspondente."""
        if instr == SOLPI_ISA.LOAD_TENSOR:
            self.registers[args['reg']] = args['data']
        
        elif instr == SOLPI_ISA.MATMUL:
            a = self.registers[args['in_a']]
            b = self.registers[args['in_b']]
            self.registers[args['out']] = np.dot(a, b)
            
        elif instr == SOLPI_ISA.RMS_NORM:
            x = self.registers[args['in']]
            # Chama a camada de normalização
            self.registers[args['out']] = self.brain.native_core.final_norm.forward(x)
            
        elif instr == SOLPI_ISA.SOFTMAX:
            x = self.registers[args['in']]
            self.registers[args['out']] = self.brain.native_core.softmax(x)
            
        return "SUCCESS"
