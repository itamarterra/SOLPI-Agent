from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_path = "E:/SOLPI-MODELS/qwen"

print(f"🚀 Carregando modelo de {model_path}...")
try:
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

    prompt = "Explique o que é o GLPI e como o SOLPI ajuda a automatizá-lo."
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    print("🧠 Gerando resposta...")
    output = model.generate(**inputs, max_new_tokens=200)

    print("\n--- RESPOSTA ---")
    print(tokenizer.decode(output[0], skip_special_tokens=True))
except Exception as e:
    print(f"❌ Erro ao testar modelo: {e}")
