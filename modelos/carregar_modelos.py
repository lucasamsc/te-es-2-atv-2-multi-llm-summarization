import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Dicionário com os caminhos locais dos modelos
MODEL_NAMES = {
    "bart": "C:/TE-ES-1/Atividades/modelos/bart-large-cnn",
    "t5": "C:/TE-ES-1/Atividades/modelos/t5-small",
    "pegasus": "C:/TE-ES-1/Atividades/modelos/pegasus-xsum"
}


def carregar_modelo(nome_modelo):
    """
    Carrega o modelo e o tokenizador para sumarização.

    Args:
        nome_modelo (str): Nome do modelo a ser carregado. Deve estar presente em `MODEL_NAMES`.

    Returns:
        tuple: (modelo, tokenizador) carregados do Hugging Face Transformers.
    """
    if nome_modelo not in MODEL_NAMES:
        raise ValueError(f"❌ Erro: O modelo '{nome_modelo}' não está definido em MODEL_NAMES!")

    caminho_modelo = MODEL_NAMES[nome_modelo]

    print(f"Carregando modelo local: {nome_modelo}")

    # Carregar tokenizador
    tokenizador = AutoTokenizer.from_pretrained(caminho_modelo, local_files_only=True)

    # Carregar modelo
    modelo = AutoModelForSeq2SeqLM.from_pretrained(
        caminho_modelo,
        torch_dtype=torch.float32,  # Evita erro de meta tensor
        device_map=None,  # Remove mapeamento automático para evitar erro de alocação
        local_files_only=True
    )

    return modelo, tokenizador