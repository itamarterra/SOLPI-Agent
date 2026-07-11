class SOLPI_ISA:
    """
    PACOTE 3080: NEURAL INSTRUCTION SET v1.0
    Define o vocabulário de baixo nível da SOLPI VM.
    Inspirado em arquiteturas de CPU/GPU.
    """
    # Instruções de Dados
    LOAD_TENSOR = "LOAD_T"
    STORE_TENSOR = "STORE_T"
    
    # Instruções Matemáticas (Kernels)
    MATMUL = "MATMUL"
    ADD_RESID = "ADD_RES"
    RMS_NORM = "RMS_NORM"
    
    # Instruções Específicas de Transformer
    ATTENTION_GQA = "ATTN_GQA"
    ROPE_ROTATE = "ROPE_ROT"
    SOFTMAX = "SOFTMAX"
    SWIGLU = "SWIGLU"
    
    # Controle de Fluxo
    SYNC_STREAM = "SYNC"
    EXIT = "HALT"
