import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from configuracoes import MODEL_NAMES

# Carrega o modelo e o tokenizador a partir de um diretório local.
def carregar_modelo(nome_modelo):
    print(f"-> Carregando modelo local: {nome_modelo}")

    tokenizador = AutoTokenizer.from_pretrained(MODEL_NAMES[nome_modelo], local_files_only=True)
    modelo = AutoModelForCausalLM.from_pretrained(
        MODEL_NAMES[nome_modelo],
        torch_dtype=torch.float16,  # Usa menor precisão para economizar VRAM
        device_map="auto",  # Mapeia automaticamente para CPU/GPU
        local_files_only=True  # Garante que não tente baixar arquivos online
    )

    return modelo, tokenizador
