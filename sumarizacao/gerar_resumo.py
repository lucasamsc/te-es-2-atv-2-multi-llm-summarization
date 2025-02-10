from transformers import pipeline
from modelos.carregar_modelos import carregar_modelo
from sumarizacao.processamento_texto import dividir_texto

def gerar_resumo(texto, nome_modelo):
    """
    Gera um resumo usando o modelo especificado.

    Args:
        texto (str): Texto a ser resumido.
        nome_modelo (str): Nome do modelo (ex: "bart", "t5", "pegasus").

    Returns:
        str: Resumo gerado pelo modelo.
    """
    print(f"Carregando modelo local: {nome_modelo}")
    modelo, tokenizador = carregar_modelo(nome_modelo)

    pipeline_resumo = pipeline("summarization", model=modelo, tokenizer=tokenizador)

    trechos = dividir_texto(texto)

    resumo = pipeline_resumo(
        trechos,
        min_length=20,
        max_length=150,
        truncation=True
    )

    return " ".join([r["summary_text"] for r in resumo])
