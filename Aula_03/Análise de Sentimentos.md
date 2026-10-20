

# 🧠 Atividade: Análise de Sentimentos e os Segredos do PLN

**Objetivo:** Explorar como a Inteligência Artificial utiliza o **Processamento de Linguagem Natural (PLN)** para entender não apenas palavras, mas o contexto e a intenção das frases em Português.

---

## 📚 Parte 1: O que é PLN (Processamento de Linguagem Natural)?

O **PLN** (ou **NLP** em inglês) é o campo da IA que dá aos computadores a capacidade de ler, entender e derivar significado das línguas humanas. Para que o código que você vai rodar funcione, a IA realiza três processos fundamentais de PLN:

### 1. Tokenização (Fatiar o texto)
O computador não lê uma frase inteira de uma vez. Primeiro, ele a "fatia" em unidades menores chamadas **Tokens**. 
*   *Exemplo:* "Eu não gosto" vira `['Eu', 'não', 'gosto']`. Isso permite que a IA analise cada peça individualmente antes de entender o todo.

### 2. Embeddings (Transformar palavras em números)
Computadores só entendem números. O PLN usa uma técnica chamada **Embeddings** para converter palavras em vetores (listas de números). 
*   Nesse mapa matemático, palavras com significados parecidos (como "alegre" e "feliz") ficam localizadas próximas uma da outra, permitindo que a IA entenda sinônimos.

### 3. Atenção e Contexto (Transformers/BERT)
Esta é a parte mais avançada. O modelo que usaremos (BERT) usa um mecanismo chamado **Atenção**. Ele analisa a relação entre todas as palavras da frase ao mesmo tempo. 
*   *Por que isso importa?* Na frase "Eu não estou bem", a IA "presta atenção" no **não**, entendendo que ele inverte totalmente o significado da palavra **bem**. IAs antigas ignoravam isso; o PLN moderno não.

---

## 💻 Parte 2: A Prática (Mão no Código)

Siga os passos no seu Google Colab para ver o PLN em ação.

### Passo 1: Instalação
*Vamos instalar o `pysentimiento`, uma biblioteca de última geração para PLN em Português.*

```python
# Instalando a biblioteca de Deep Learning (PLN Profundo)
!pip install pysentimiento --quiet
print("Cérebro de PLN instalado com sucesso!")
```

### Passo 2: O Analisador de Sentimentos Interativo
```python
from pysentimiento import create_analyzer

# Inicializa o analisador para Português (pt)
# Ele carregará o modelo BERT treinado com milhões de frases reais
print("Carregando motor de PLN... (aguarde o download do modelo)")
analyzer = create_analyzer(task="sentiment", lang="pt")

def iniciar_analise():
    print("\n" + "="*45)
    print("      LABORATÓRIO DE PLN - SENTIMENTOS")
    print("="*45)
    
    frase = input("Digite uma frase (pode usar gírias e emojis): ")
    
    if not frase:
        return

    # A IA realiza a Tokenização, Embedding e Análise de Contexto aqui:
    resultado = analyzer.predict(frase)
    
    # Mapeamento para exibição
    mapa = {
        'POS': ('✅ POSITIVO', '\033[92m'),
        'NEG': ('❌ NEGATIVO', '\033[91m'),
        'NEU': ('😐 NEUTRO', '\033[94m')
    }
    
    nome, cor = mapa[resultado.output]
    confianca = resultado.probas[resultado.output] * 100

    print(f"\nANÁLISE FINAL:")
    print(f"Texto analisado: \"{frase}\"")
    print(f"Classificação: {cor}{nome}\033[0m")
    print(f"Confiança da IA: {confianca:.2f}%")
    
    # Visualizando a distribuição de probabilidade (o 'pensamento' da IA)
    print("\nProbabilidades por categoria:")
    for sent, prob in resultado.probas.items():
        barra = "█" * int(prob * 20)
        print(f"{sent}: {barra} {prob*100:.1f}%")

# Executar a ferramenta
iniciar_analise()
```

---

## ✍️ Parte 3: Desafios de PLN (Exercícios)

Use o campo de digitação do código acima para investigar como o PLN funciona:

1.  **O Desafio do Contexto:** Digite *"Eu estou bem"* e depois *"Eu não estou nada bem"*. 
    *   *Observação:* Veja como a IA mudou o resultado drasticamente apenas por causa de um modificador (o "não"). Isso é o mecanismo de **Atenção** funcionando.

2.  **O Desafio dos Emojis:** Digite apenas emojis, como `😊` ou `💀`. 
    *   *Pergunta:* O PLN consegue entender sentimentos sem nenhuma palavra escrita? Como as probabilidades se comportam?

3.  **O Desafio da Ambiguidade:** Digite uma frase neutra, como *"O céu é azul"* ou *"Eu comprei um pão"*.
    *   *Observação:* Note que a confiança da IA para "NEU" (Neutro) deve ser alta. O PLN é capaz de identificar quando não há emoção envolvida.

4.  **O Desafio da Ironia:** Tente enganar a IA com sarcasmo: *"Que ótimo, meu computador quebrou logo hoje!"*.
    *   *Pergunta:* O modelo BERT foi capaz de entender que a situação é negativa, mesmo com a palavra "ótimo" no início?

---

## 🏁 Conclusão
O **PLN** é o que permite que a tecnologia nos entenda de forma humana. O que você usou hoje não é apenas um código de "se... então", mas uma rede neural complexa que aprendeu as nuances, as gírias e as estruturas da nossa língua através de bilhões de exemplos matemáticos.