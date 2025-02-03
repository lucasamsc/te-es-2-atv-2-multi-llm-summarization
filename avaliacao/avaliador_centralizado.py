from transformers import pipeline
from modelos.carregar_modelos import carregar_modelo

# Avalia os resumos gerados e escolhe o melhor com base na concisão e precisão.
def avaliar_resumos(resumos):
    modelo, tokenizador = carregar_modelo("llama")
    pipeline_avaliacao = pipeline("text-generation", model=modelo, tokenizer=tokenizador)

    prompt_avaliacao = "Avalie os seguintes resumos e escolha o melhor com base em:\n"
    prompt_avaliacao += "- Clareza e precisão\n"
    prompt_avaliacao += "- Concisão (máximo de 6 palavras)\n"
    prompt_avaliacao += "- Cobertura da informação essencial\n\n"

    for idx, resumo in enumerate(resumos):
        prompt_avaliacao += f"Resumo {idx + 1}: {resumo}\n"
    prompt_avaliacao += "\nEscolha o melhor resumo e explique sua escolha."

    resultado_avaliacao = pipeline_avaliacao(
        prompt_avaliacao,
        max_new_tokens=10,  # Reduzindo o tamanho da resposta
        truncation=True,
        do_sample=False  # Agora tornando a resposta determinística
    )[0]["generated_text"]

    # Processar a resposta para pegar apenas o resumo escolhido
    melhor_resumo = processar_resposta_avaliacao(resultado_avaliacao, resumos)

    return melhor_resumo


def processar_resposta_avaliacao(resposta, resumos):
    """
    Processa a resposta do modelo para extrair o resumo escolhido.
    """
    for idx, resumo in enumerate(resumos):
        if f"Resumo {idx + 1}" in resposta:
            return resumo  # Retorna o resumo escolhido pelo modelo
    return min(resumos, key=len)  # Se o modelo não escolher claramente, retorna o mais curto