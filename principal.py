import os
import json
from sumarizacao.gerar_resumo import gerar_resumo
from avaliacao.calcular_metricas import calcular_metricas
from avaliacao.avaliador_centralizado import avaliar_resumos
from sumarizacao.descentralizado import avaliar_resumos_descentralizado

# Definição dos diretórios
PASTA_ENTRADA = "dados/textos_entrada/"
PASTA_RESUMOS = "dados/resumos/"
PASTA_AVALIACAO = "dados/avaliacoes/"

# Criar diretórios caso não existam
os.makedirs(PASTA_RESUMOS, exist_ok=True)
os.makedirs(PASTA_AVALIACAO, exist_ok=True)

# Processar cada arquivo de entrada
for arquivo in os.listdir(PASTA_ENTRADA):
    caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    print(f"\n🔹 Gerando resumo para: {arquivo}")
    resumos = [gerar_resumo(texto, modelo) for modelo in ["llama", "gemma"]]

    # Salvar resumos gerados
    for i, modelo in enumerate(["llama", "gemma"]):
        caminho_resumo = os.path.join(PASTA_RESUMOS, f"{modelo}_{arquivo}")
        with open(caminho_resumo, "w", encoding="utf-8") as f:
            f.write(resumos[i])

    print("-> Resumos salvos com sucesso!")

    # Avaliação Centralizada (um modelo escolhe o melhor resumo)
    melhor_resumo_central = avaliar_resumos(resumos)

    # Avaliação Descentralizada (os modelos avaliam os resumos uns dos outros)
    melhor_resumo_descentral = avaliar_resumos_descentralizado(resumos)

    # Definir um resumo de referência (pode ser ajustado depois)
    referencia = "Resumo de referência esperado."

    # Calcular métricas ROUGE e BLEU
    avaliacao_centralizada = calcular_metricas(referencia, melhor_resumo_central)
    avaliacao_descentralizada = calcular_metricas(referencia, melhor_resumo_descentral)

    print("\nAvaliação Centralizada:", avaliacao_centralizada)
    print("Avaliação Descentralizada:", avaliacao_descentralizada)

    # Salvar as avaliações
    caminho_avaliacao_central = os.path.join(PASTA_AVALIACAO, f"avaliacao_centralizada_{arquivo}.json")
    caminho_avaliacao_descentral = os.path.join(PASTA_AVALIACAO, f"avaliacao_descentralizada_{arquivo}.json")

    with open(caminho_avaliacao_central, "w", encoding="utf-8") as f:
        json.dump(avaliacao_centralizada, f, indent=4, ensure_ascii=False)

    with open(caminho_avaliacao_descentral, "w", encoding="utf-8") as f:
        json.dump(avaliacao_descentralizada, f, indent=4, ensure_ascii=False)

    print(f"✅ Avaliações salvas com sucesso: {caminho_avaliacao_central}, {caminho_avaliacao_descentral}")