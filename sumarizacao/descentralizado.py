def avaliar_resumos_descentralizado(resumos):
    """
    Implementação descentralizada onde cada modelo avalia os resumos gerados pelos outros.

    Args:
        resumos (list): Lista de resumos gerados.

    Returns:
        str: O melhor resumo escolhido pelo processo descentralizado.
    """
    votos = {}
    for i, resumo_avaliado in enumerate(resumos):
        votos[i] = 0
        for j, avaliador in enumerate(resumos):
            if i != j:
                votos[i] += 1 if len(resumo_avaliado) < len(avaliador) else 0

    melhor_resumo = max(votos, key=votos.get)
    return resumos[melhor_resumo]