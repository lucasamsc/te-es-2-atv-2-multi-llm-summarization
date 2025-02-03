from transformers import pipeline
from modelos.carregar_modelos import carregar_modelo
from sumarizacao.processamento_texto import dividir_texto


def gerar_resumo(texto, nome_modelo):
    """
    Gera um resumo usando o modelo especificado.

    Args:
        texto (str): Texto a ser resumido.
        nome_modelo (str): Nome do modelo (ex: "llama", "gemma").

    Returns:
        str: Resumo gerado pelo modelo.
    """
    print(f"🔹 Carregando modelo local: {nome_modelo}")
    modelo, tokenizador = carregar_modelo(nome_modelo)

    pipeline_resumo = pipeline(
        "text-generation",
        model=modelo,
        tokenizer=tokenizador
    )

    trechos = dividir_texto(texto)

    # Definir um prompt claro para limitar o tamanho do resumo
    prompt = "Resuma o seguinte texto em **EXATAMENTE 6 palavras** sem adicionar detalhes desnecessários:\n\n"

    resumos = [
        pipeline_resumo(prompt + chunk, max_new_tokens=4, truncation=True, do_sample=True, temperature=0.1, top_p=0.5)[
            0]["generated_text"]
        for chunk in trechos
    ]

    return " ".join(resumos)
