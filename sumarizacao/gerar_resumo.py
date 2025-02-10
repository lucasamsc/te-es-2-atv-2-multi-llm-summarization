from transformers import pipeline
from modelos.carregar_modelos import carregar_modelo

def gerar_resumo(texto, nome_modelo, rounds=2):
    """
    Gera um resumo para um determinado texto utilizando múltiplos rounds de refinamento.
    """
    modelo, tokenizador = carregar_modelo(nome_modelo)
    sumarizador = pipeline("summarization", model=modelo, tokenizer=tokenizador)

    resumo_atual = texto  # Começa com o texto original

    for _ in range(rounds):
        resumo_gerado = sumarizador(resumo_atual, max_length=150, min_length=50, do_sample=False)[0]["summary_text"]
        resumo_atual = resumo_gerado  # Atualiza o resumo para a próxima iteração

    return resumo_atual
