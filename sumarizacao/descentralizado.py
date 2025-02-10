import random
# Avaliação descentralizada dos resumos: cada modelo vota no melhor resumo.
def avaliar_resumos_descentralizado(resumos):
    votos = {i: 0 for i in range(len(resumos))}  # Inicializa contagem de votos

    for _ in range(3):  # Simula 3 modelos participando da avaliação
        melhor_resumo_idx = random.randint(0, len(resumos) - 1)  # Escolha aleatória simulando avaliação
        votos[melhor_resumo_idx] += 1

    melhor_resumo = resumos[max(votos, key=votos.get)]  # Pega o mais votado

    return melhor_resumo
