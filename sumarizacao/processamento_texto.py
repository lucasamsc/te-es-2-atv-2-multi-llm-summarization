import nltk
from nltk.tokenize import sent_tokenize
from configuracoes import TAMANHO_MAX_CHUNK

nltk.download('punkt')

# Divide o texto em trechos menores para evitar estourar o limite do modelo.
def dividir_texto(texto):
    frases = sent_tokenize(texto)
    trechos = []
    trecho_atual = ""

    for frase in frases:
        if len(trecho_atual) + len(frase) < TAMANHO_MAX_CHUNK:
            trecho_atual += " " + frase
        else:
            trechos.append(trecho_atual.strip())
            trecho_atual = frase

    if trecho_atual:
        trechos.append(trecho_atual.strip())

    return trechos
