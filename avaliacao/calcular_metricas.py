from evaluate import load

# Calcula as métricas ROUGE e BLEU comparando o resumo gerado com o de referência.
def calcular_metricas(referencia, gerado):
    rouge = load("rouge")
    bleu = load("bleu")

    # Cálculo das métricas
    rouge_scores = rouge.compute(predictions=[gerado], references=[referencia])
    bleu_scores = bleu.compute(predictions=[gerado], references=[referencia])

    return {"rouge": rouge_scores, "bleu": bleu_scores}
