import os
from modelos.carregar_modelos import carregar_modelo
from modelos.carregar_modelos import MODEL_NAMES
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

# Lista de modelos de sumarização
modelos_para_testar = ["bart", "t5", "pegasus"]

# Processar cada arquivo de entrada
for arquivo in os.listdir(PASTA_ENTRADA):
    caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    print("\n" + "=" * 60)
    print(f"**Processando Arquivo:** {arquivo}")
    print("=" * 60)

    # Carregar os modelos uma única vez e mostrar progresso
    modelos_carregados = {}
    for modelo in modelos_para_testar:
        print(f"Carregando modelo **{modelo.upper()}**...")
        modelos_carregados[modelo] = carregar_modelo(modelo)

    print("\n**Todos os modelos carregados!** Iniciando a geração dos resumos...\n")

    # Gerar resumos e exibir progresso
    resumos = []
    for modelo in modelos_para_testar:
        print(f"**Gerando resumo com {modelo.upper()}**...")
        resumo = gerar_resumo(texto, modelo)
        resumos.append(resumo)

        # Salvar resumos gerados
        caminho_resumo = os.path.join(PASTA_RESUMOS, f"{modelo}_{arquivo}")
        with open(caminho_resumo, "w", encoding="utf-8") as f:
            f.write(resumo)

    print("\n**Resumos gerados e salvos!**\n")

    # Avaliação Centralizada
    print("**Realizando Avaliação Centralizada...**")
    melhor_resumo_central = avaliar_resumos(resumos)

    # Avaliação Descentralizada
    print("**Realizando Avaliação Descentralizada...**")
    melhor_resumo_descentral = avaliar_resumos_descentralizado(resumos)

    # Definir um resumo de referência (pode ser ajustado depois)
    referencia = "Resumo de referência esperado."

    # Calcular métricas ROUGE e BLEU
    print("\n**Calculando métricas ROUGE e BLEU...**")
    avaliacao_centralizada = calcular_metricas(referencia, melhor_resumo_central)
    avaliacao_descentralizada = calcular_metricas(referencia, melhor_resumo_descentral)

    print("\n" + "=" * 60)
    print("**Resultados das Avaliações**")
    print("=" * 60)

    print("\n**Avaliação Centralizada:**")
    print(f"**ROUGE-1:** {avaliacao_centralizada['rouge']['rouge1']:.4f}")
    print(f"**ROUGE-2:** {avaliacao_centralizada['rouge']['rouge2']:.4f}")
    print(f"**ROUGE-L:** {avaliacao_centralizada['rouge']['rougeL']:.4f}")
    print(f"**BLEU Score:** {avaliacao_centralizada['bleu']['bleu']:.4f}")

    print("\n**Avaliação Descentralizada:**")
    print(f"**ROUGE-1:** {avaliacao_descentralizada['rouge']['rouge1']:.4f}")
    print(f"**ROUGE-2:** {avaliacao_descentralizada['rouge']['rouge2']:.4f}")
    print(f"**ROUGE-L:** {avaliacao_descentralizada['rouge']['rougeL']:.4f}")
    print(f"**BLEU Score:** {avaliacao_descentralizada['bleu']['bleu']:.4f}")

    print("\n**Processamento concluído para o arquivo:**", arquivo)
    print("=" * 60 + "\n")