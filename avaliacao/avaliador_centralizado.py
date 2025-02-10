from transformers import pipeline
from modelos.carregar_modelos import carregar_modelo
from avaliacao.calcular_metricas import calcular_metricas

def avaliar_resumos(resumos):
    modelo, tokenizador = carregar_modelo("bart")
    pipeline_avaliacao = pipeline("summarization", model=modelo, tokenizer=tokenizador)

    prompt_avaliacao = "Avalie os seguintes resumos e escolha o melhor com base em:\n"
    prompt_avaliacao += "- Clareza e precisão\n"
    prompt_avaliacao += "- Concisão (máximo de 6 palavras)\n"
    prompt_avaliacao += "- Cobertura da informação essencial\n\n"

    for idx, resumo in enumerate(resumos):
        prompt_avaliacao += f"Resumo {idx+1}: {resumo}\n"
    prompt_avaliacao += "\nEscolha o melhor resumo e explique sua escolha."

    # Criar dicionário associando cada resumo às suas métricas
    referencia = "Resumo de referência esperado."
    resumos_avaliados = {resumo: calcular_metricas(referencia, resumo) for resumo in resumos}

    def calcular_pontuacao_avaliacao(metrica):
        rouge = metrica.get("rouge", {})
        bleu = metrica.get("bleu", {})
        return (rouge.get("rougeLsum", 0) * 0.6) + (bleu.get("bleu", 0) * 0.4)

    # Escolhe o melhor resumo baseado nas métricas
    melhor_resumo = max(resumos_avaliados, key=lambda r: calcular_pontuacao_avaliacao(resumos_avaliados[r]))

    return melhor_resumo