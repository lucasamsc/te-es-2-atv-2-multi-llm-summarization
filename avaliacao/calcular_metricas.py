from evaluate import load

def calcular_metricas(referencia, gerado):
    """
    Calcula as métricas ROUGE e BLEU comparando o resumo gerado com o de referência.

    Args:
        referencia (str): Texto de referência para avaliação.
        gerado (str): Resumo gerado pelo modelo.

    Returns:
        dict: Dicionário com os resultados de ROUGE e BLEU.
    """
    rouge = load("rouge")
    bleu = load("bleu")

    # Cálculo das métricas
    rouge_scores = rouge.compute(predictions=[gerado], references=[referencia])
    bleu_scores = bleu.compute(predictions=[gerado], references=[referencia])

    return {"rouge": rouge_scores, "bleu": bleu_scores}
