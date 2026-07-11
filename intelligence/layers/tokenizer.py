import json
import os

class SOLPITokenizer:
    """
    PACOTE 6500: TOKENIZER ENGINE v50.0
    Converte texto em IDs e vice-versa com suporte a vocabulário dinâmico.
    """
    def __init__(self, vocab_path="E:/SOLPI-DATA/vocabulary.json"):
        self.vocab_path = vocab_path
        self.vocab = {"<PAD>": 0, "<UNK>": 1, "<BOS>": 2, "<EOS>": 3}
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self._load_vocab()

    def _load_vocab(self):
        if os.path.exists(self.vocab_path):
            with open(self.vocab_path, 'r', encoding='utf-8') as f:
                self.vocab = json.load(f)
                self.inv_vocab = {int(v): k for k, v in self.vocab.items()}

    def encode(self, text):
        """Conversão simples para IDs (Simulação de Byte-Pair Encoding)."""
        tokens = []
        for word in text.split():
            if word not in self.vocab:
                # Aprende novas palavras dinamicamente para expansão
                if len(self.vocab) < 10000: # Limite
                    new_id = len(self.vocab)
                    self.vocab[word] = new_id
                    self.inv_vocab[new_id] = word
            tokens.append(self.vocab.get(word, self.vocab["<UNK>"]))
        return tokens

    def decode(self, ids):
        return " ".join([self.inv_vocab.get(int(i), "<UNK>") for i in ids])
