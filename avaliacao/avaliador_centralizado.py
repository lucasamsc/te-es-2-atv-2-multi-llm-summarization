from transformers import pipeline
from modelos.carregar_modelos import carregar_modelo

# Avalia os resumos e escolhe o melhor com base nos critérios do artigo.
def avaliar_resumos(resumos):
    modelo, tokenizador = carregar_modelo("bart")
    pipeline_avaliacao = pipeline("summarization", model=modelo, tokenizer=tokenizador)

    prompt_avaliacao = (
        "Dado o conjunto de resumos abaixo, escolha aquele que melhor representa o conteúdo original.\n\n"
        "Critérios:\n"
        "- Clareza e precisão\n"
        "- Concisão (máximo de 6 palavras)\n"
        "- Cobertura da informação essencial\n\n"
    )

    for idx, resumo in enumerate(resumos):
        prompt_avaliacao += f"Resumo {idx + 1}: {resumo}\n"

    prompt_avaliacao += "\nIndique o número do melhor resumo e explique a escolha."

    resultado_avaliacao = pipeline_avaliacao(prompt_avaliacao, max_length=50, truncation=True)[0]["summary_text"]

    return resultado_avaliacao
