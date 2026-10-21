## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# PIPELINE DE PROCESSAMENTO DE LINGUAGEM NATURAL (PLN COM BERT)
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

!pip install -q pysentimiento

from pysentimiento import create_analyzer

# 1. Instanciação do analisador para língua portuguesa
analyzer = create_analyzer(task="sentiment", lang="pt")

# 2. Amostras para teste automatizado em lote
avaliacoes = [
    "O atendimento da cantina foi excepcional!",
    "Péssima experiência, atrasou mais de 2 horas e veio frio.",
    "O pacote contém 50 unidades de parafusos sextavados.",
    "Não achei o produto de todo ruim, até que supriu a necessidade.",
    "Que maravilha, cancelaram meu voo em cima da hora 👏😡"
]

print("=== RELATÓRIO DE MONITORAMENTO DE SENTIMENTOS (BERT PT-BR) ===\n")
for texto in avaliacoes:
    pred = analyzer.predict(texto)
    print(f"Texto: \"{texto}\"")
    print(f"Sentimento: {pred.output} | Probabilidades: POS={pred.probas['POS']:.2f}, NEG={pred.probas['NEG']:.2f}, NEU={pred.probas['NEU']:.2f}\n")
```
