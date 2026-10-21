# 💬 Laboratório Prático: Análise de Sentimentos com BERT & PLN — Monitorando a Voz do Cliente

**Ambiente:** Google Colaboratory (`Python 3.10+`)  
**Modalidade:** Processamento de Linguagem Natural Profundo (*Deep Learning / Transformers / BERT*)  
**Tempo Estimado:** 35 a 45 minutos  
**Biblioteca / Modelo:** `pysentimiento` (Modelo RoBERTa / BERT especializado em língua portuguesa)  
**Classes de Sentimento:** `POS` (Positivo), `NEG` (Negativo) e `NEU` (Neutro)

---

## 📋 1. ENUNCIADO DA ATIVIDADE (CONTEXTO DE NEGÓCIO)

> ### 📢 Desafio: Monitoramento de Reputação e SAC Automatizado (InovaMarketplace)
> O setor de atendimento ao cliente do **InovaMarketplace** recebe mais de 20 mil comentários, tweets e avaliações de produtos diariamente. A diretoria necessita de um sistema de Inteligência Artificial capaz de analisar instantaneamente o sentimento das mensagens recebidas e priorizar casos de clientes revoltados para o time humano de retenção.
>
> Algoritmos antigos baseados em contagem simples de palavras (*Bag of Words*) falham miseravelmente diante de **negações** (*"Não achei nada bom"*), **emojis** (*"A entrega demorou 😡"*), **gírias** e, principalmente, **ironia/sarcasmo** (*"Maravilha, o produto chegou todo quebrado!"*).
>
> **Sua Missão:**
> 1. Configurar um pipeline de PLN moderno no Google Colab utilizando o modelo **BERT / RoBERTa** da biblioteca `pysentimiento`.
> 2. Compreender os 3 pilares técnicos: **Tokenização por subpalavras**, **Embeddings Vetoriais** e o mecanismo de **Auto-Atenção (*Self-Attention*)**.
> 3. Construir uma função de análise de sentimentos interativa que extraia a classe dominante e a distribuição percentual de probabilidades.
> 4. Submeter a IA aos **4 testes de estresse linguísticos** (Inversão de contexto, Emojis, Neutralidade e Sarcasmo).
> 5. Interpretar as limitações dos modelos de linguagem e sugerir boas práticas para mitigação de falsos diagnósticos.

---

## 🛠️ 2. PASSO A PASSO DETALHADO DO LABORATÓRIO

```mermaid
flowchart LR
    TXT["1. Texto do Cliente\n'O produto não é ruim!'"] --> TOK["2. Tokenização\n['O', 'produto', 'não', 'é', 'ruim', '!']"]
    TOK --> EMB["3. Embeddings\n(Vetores Numéricos em 768 Dimensões)"]
    EMB --> ATT["4. Self-Attention (BERT)\n(O 'não' se conecta ao 'ruim')"]
    ATT --> OUT["5. Probabilidades\nPOS: 68% | NEU: 25% | NEG: 7%"]
```

### Passo 1: Os 3 Pilares do Processamento de Linguagem Natural Moderno

| Pilar | Nome Técnico | O que ele faz nos bastidores? |
| :--- | :---: | :--- |
| **1º Pilar** | **Tokenização (*WordPiece/BPE*)** | O computador fatia a frase em pedaços atômicos (tokens). Palavras raras ou compostas são divididas para que a IA nunca trave diante de vocabulário novo. |
| **2º Pilar** | **Embeddings Vetoriais** | Converte cada token em uma lista de números (vetor). Palavras com semântica próxima ocupam coordenadas vizinhas no hiperespaço. |
| **3º Pilar** | **Auto-Atenção (*Self-Attention*)** | Permite que cada palavra "olhe" para todas as outras palavras da frase simultaneamente, descobrindo quem modifica quem (ex.: o *"não"* alterando *"ruim"*). |

---

### Passo 2: Instalação e Carregamento do Cérebro BERT
No Google Colab, instale a biblioteca `pysentimiento`:

```python
!pip install -q pysentimiento

from pysentimiento import create_analyzer
import matplotlib.pyplot as plt

print("Carregando o modelo BERT treinado em Português... (aguarde alguns segundos)")
analisador = create_analyzer(task="sentiment", lang="pt")
print("✅ Motor de PLN pronto para análise!")
```

---

### Passo 3: Criando a Função de Diagnóstico Visual
Criamos uma função que recebe a frase e plota a distribuição percentual de certeza da IA:

```python
def analisar_sentimento_completo(texto):
    resultado = analisador.predict(texto)
    sentimento = resultado.output
    probabilidades = resultado.probas
    
    mapa_rotulos = {'POS': 'Positivo 😊', 'NEG': 'Negativo 😡', 'NEU': 'Neutro 😐'}
    cores = {'POS': '#10B981', 'NEG': '#EF4444', 'NEU': '#64748B'}
    
    print("\n" + "="*50)
    print(f"Frase Analisada: \"{texto}\"")
    print(f"Diagnóstico da IA: {mapa_rotulos[sentimento]}")
    print(f"Confiança: {probabilidades[sentimento]*100:.2f}%")
    print("="*50)
    
    # Gráfico de barras das probabilidades
    classes = list(mapa_rotulos.values())
    valores = [probabilidades['POS'], probabilidades['NEG'], probabilidades['NEU']]
    
    plt.figure(figsize=(6, 3))
    barras = plt.bar(classes, [v*100 for v in valores], color=['#10B981', '#EF4444', '#64748B'])
    plt.ylabel("Probabilidade (%)")
    plt.title("Distribuição de Certeza do Modelo BERT")
    plt.ylim(0, 100)
    
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2., altura + 2, f'{altura:.1f}%', ha='center', va='bottom')
        
    plt.tight_layout()
    plt.show()

# Teste inicial
analisar_sentimento_completo("Adorei o produto, entrega super rápida e excelente acabamento!")
```

---

## 🧪 3. EXPERIMENTO CIENTÍFICO: OS 4 TESTES DE ESTRESSE LINGUÍSTICOS

Submeta o modelo aos **4 desafios fundamentais da linguagem humana** e registre as probabilidades no seu relatório:

### Desafio 1: Inversão de Contexto e Negação
* Frase A: `"Este filme é bom."`
* Frase B: `"Este filme não é bom."`
* Frase C: `"Este filme não é ruim!"`
* *O que observar:* Como o mecanismo de *Self-Attention* lida com a palavra "não"? A Frase C foi classificada como Positiva?

### Desafio 2: O Poder Semântico dos Emojis
* Frase A: `"Chegou hoje"`
* Frase B: `"Chegou hoje 😍"`
* Frase C: `"Chegou hoje 😡"`
* *O que observar:* Os emojis alteram radicalmente o sentimento mesmo sem nenhuma palavra adjetiva!

### Desafio 3: A Linha Tênue da Neutralidade
* Frase: `"O pedido foi entregue na portaria às 14h30 pelo carteiro."`
* *O que observar:* O modelo identificou corretamente a classe `NEU` com mais de 80% de certeza?

### Desafio 4: O Teste Supremo — Ironia e Sarcasmo
* Frase A: `"Parabéns pelo atendimento maravilhoso! Esperando há apenas 4 horas na fila."`
* Frase B: `"Que legal, meu celular caiu no chão e a tela virou farinha."`
* *O que observar:* O BERT conseguiu identificar o sarcasmo ou foi enganado pelas palavras *"maravilhoso"* e *"legal"*?

---

## 💻 4. CÓDIGO FONTE COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

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

---

## ✅ 5. ENTREGÁVEL DA ATIVIDADE (CHECKLIST DE CONCLUSÃO)

Para validar a conclusão deste laboratório, certifique-se de preencher os itens:
- [ ] Biblioteca `pysentimiento` instalada e modelo BERT carregado no Colab.
- [ ] Função de diagnóstico visual executada com gráfico de probabilidades.
- [ ] Os 4 testes de estresse (Negação, Emojis, Neutralidade e Sarcasmo) executados.
- [ ] Análise documentada: *Por que modelos clássicos de contagem de palavras falham com negações e como a arquitetura Transformer soluciona esse problema?*