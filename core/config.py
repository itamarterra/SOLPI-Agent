class SOLPIConfig:
    """
    CONFIGURAÇÃO DA IA v25.0 (Etapa 3 do Guia)
    Define a 'receita' do cérebro.
    """
    # Arquitetura
    VOCAB_SIZE = 5000
    EMBED_DIM = 256
    NUM_HEADS = 8
    NUM_KV_HEADS = 2 # Para GQA (v40.0)
    NUM_LAYERS = 4
    MAX_SEQ_LEN = 512
    
    # Treinamento
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    EPOCHS = 10
    
    # Caminhos e Modelos (Fase 1)
    MODEL_TYPE = "native" # "native" ou "transformers"
    MODEL_PATH = "models/qwen"
    DEVICE = "auto"
    
    # Caminhos
    WEIGHTS_PATH = "brain_weights.npy"
    KNOWLEDGE_DIR = "knowledge"
