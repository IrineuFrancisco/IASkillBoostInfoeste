# 🌸 Guia de Aula (Code): Aprendizado Não Supervisionado com o Dataset Iris

**Curso:** Aperfeiçoamento Profissional em Programação em Inteligência Artificial Generativa (SENAI-SP)  
**Unidade / Aula:** Aula 01 — Laboratório 2 (Clusterização com `K-Means`)  
**Ambiente:** Google Colaboratory (`Python 3.10+`)  
**Arquivo Necessário:** Faça o upload do arquivo [`iris.csv`](file:///C:/Apps/Curso%20ia/Curso_Organizado_SENAI/Aula_01/iris.csv) na aba lateral **Arquivos (📁)** do Google Colab antes de iniciar!

---

## 🎯 Objetivo da Prática

Entender na prática como o computador consegue identificar e separar **grupos (espécies) de flores** **sem que ninguém diga a ele quais são os nomes originais (Sem Rótulos)**, utilizando exclusivamente medidas matemáticas de comprimento e largura em centímetros.

---

## 1. 🧰 Fundamentos e Preparação de Dados

O **Aprendizado Não Supervisionado** busca padrões ocultos. No caso do **K-Means**, o objetivo matemático é agrupar os dados em **$K$ grupos (*clusters*)** onde a distância entre cada ponto e o centro do seu grupo (**centroide**) seja a menor possível.

### 🔹 Bloco 1: Importação de Dependências e Carga Inicial
Primeiro, preparamos nosso ambiente no Google Colab com as ferramentas de análise tabular (`pandas`, `numpy`), visualização gráfica (`matplotlib`, `seaborn`) e inteligência artificial (`scikit-learn`):

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

# Carregar o dataset (certifique-se de ter enviado o arquivo iris.csv no Colab)
df = pd.read_csv('/content/iris (1).csv')

# Visualização das 5 primeiras linhas dos dados brutos
print(df.head())
```

#### 🖥️ Saída do Bloco 1 no Console (`print(df.head())`):
```text
   sepal_length  sepal_width  petal_length  petal_width species
0           5.1          3.5           1.4          0.2  setosa
1           4.9          3.0           1.4          0.2  setosa
2           4.7          3.2           1.3          0.2  setosa
3           4.6          3.1           1.5          0.2  setosa
4           5.0          3.6           1.4          0.2  setosa
```

> [!NOTE]
> **Explicação do Bloco 1:**  
> O dataset possui **150 flores** medidas em centímetros através de 4 atributos morfológicos:
> * `sepal_length` e `sepal_width`: Comprimento e largura da **sépala**.
> * `petal_length` e `petal_width`: Comprimento e largura da **pétala**.
> * `species`: A espécie real (`setosa`, `versicolor` ou `virginica`), que usaremos primeiro para explorar visualmente e **removeremos no Passo 3** para desafiar a IA às cegas!

---

## 2. 👁️ Visualização Exploratória dos Dados

Antes de aplicar qualquer algoritmo de Inteligência Artificial, o Cientista de Dados precisa **enxergar a distribuição dos dados**. O gráfico de dispersão (*scatterplot*) e o *pairplot* revelam se existe uma separação geométrica natural entre as espécies.

### 🔹 Bloco 2A: Gráfico de Dispersão (Comprimento vs. Largura da Pétala)

```python
# Gráfico de Dispersão: Comprimento vs Largura da Pétala
plt.figure(figsize=(10, 6))
sb.scatterplot(x=df['petal_length'], y=df['petal_width'], hue=df['species'], palette='Set1')
sb.regplot(x=df['petal_length'], y=df['petal_width'], scatter=False, ci=None, color='blue')
plt.title('Gráfico de Dispersão Original (Com Rótulos)')
plt.xlabel('Comprimento da Pétala (cm)')
plt.ylabel('Largura da Pétala (cm)')
plt.show()
```

#### 📊 Saída Gráfica do Bloco 2A:
![Gráfico de Dispersão Original](C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/iris_dispersao_original.png)

> [!TIP]
> **O que descobrimos neste gráfico?**  
> 1. As flores da espécie **`setosa` (pontos vermelhos)** possuem pétalas bem pequenas (menores que $2\text{ cm}$) e formam uma "ilha" completamente isolada no canto inferior esquerdo!  
> 2. As espécies **`versicolor` (azul)** e **`virginica` (verde)** são maiores e crescem seguindo uma forte tendência linear positiva (indicada pela reta azul do `regplot`).

---

### 🔹 Bloco 2B: Visão Geral de Todas as Variáveis (`pairplot`)

```python
# Pairplot para visão geral cruzando todas as 4 variáveis duas a duas
sb.pairplot(df, hue="species")
```

#### 📊 Saída Gráfica do Bloco 2B:
![Pairplot Original com Espécies](C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/iris_pairplot_original.png)

> [!NOTE]
> **Por que o `sb.pairplot` é tão poderoso?**  
> Ele gera **16 gráficos simultâneos** ($4 \times 4$), cruzando cada coluna com todas as outras! Na diagonal principal, vemos as montanhas de distribuição de densidade de cada medida. Repare como nas duas últimas linhas (`petal_length` e `petal_width`) as curvas são muito mais separadas do que nas sépalas!

---

## 3. ⚙️ Implementando o K-Means ("O Cegamento dos Dados")

Chegou a hora da verdade! Aqui **removemos a coluna `species` (a resposta)** usando `df.drop("species", axis=1)` e deixamos o algoritmo **K-Means** trabalhar apenas com os números puros na matriz `X`.

### 🔹 Bloco 3: Treinamento Não Supervisionado e Agrupamento (`fit_predict`)

```python
# Preparação: Removemos o rótulo para simular o desconhecimento das espécies
X = np.array(df.drop("species", axis=1))

# Codificamos os rótulos reais apenas para comparação futura (Acurácia no Passo 4)
label_encoder = LabelEncoder()
y_true = label_encoder.fit_transform(df['species'])

# Execução do K-Means buscando k=3 grupos ocultos
k = 3
kmeans = KMeans(n_clusters=k, random_state=0)
clusters = kmeans.fit_predict(X)

# Adicionando os resultados descobertos pela IA ao DataFrame para comparar
df['k-classes'] = clusters

# Visualizando como o Algoritmo agrupou as flores por conta própria
sb.pairplot(df, hue="k-classes", palette='viridis')
```

#### 📊 Saída Gráfica do Bloco 3:
![Pairplot Agrupado pelo K-Means](C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/iris_pairplot_kmeans.png)

> [!IMPORTANT]
> **Compare este gráfico com o `pairplot` do Passo 2B!**  
> Mesmo **sem saber que existiam espécies botânicas**, o K-Means analisou as distâncias geométricas e batizou os grupos como **`0` (roxo)**, **`1` (verde-água)** e **`2` (amarelo)**, reconstruindo quase com perfeição a divisão biológica original!

---

## 4. 🎯 Avaliação de Performance (Mapeamento e Acurácia)

Em problemas reais de Aprendizado Não Supervisionado (como segmentar clientes novos de uma loja), não temos um "gabarito" para medir acurácia. Porém, como o Dataset Iris é um experimento clássico onde conhecemos as 3 espécies verdadeiras, podemos usar a biblioteca matemática `scipy` (`linear_sum_assignment`) para alinhar os números dos clusters (`0, 1, 2`) com as espécies reais e medir a precisão do agrupamento!

### 🔹 Bloco 4: Alinhamento de Clusters e Cálculo da Acurácia

```python
from scipy.optimize import linear_sum_assignment
from sklearn.metrics import accuracy_score, confusion_matrix

# Matriz de confusão para ver a relação entre os clusters gerados e as etiquetas reais
conf_matrix = confusion_matrix(y_true, clusters)

# Mapeamento matemático para alinhar os índices dos clusters com as espécies reais
row_ind, col_ind = linear_sum_assignment(-conf_matrix)
clusters_mapeados = np.zeros_like(clusters)
for i, j in zip(row_ind, col_ind):
    clusters_mapeados[clusters == i] = j

# Cálculo da Acurácia Final
acuracia = accuracy_score(y_true, clusters_mapeados)
print(f"Acurácia do Agrupamento: {acuracia * 100:.2f}%")
```

#### 🖥️ Saída do Bloco 4 no Console:
```text
Acurácia do Agrupamento: 89.33%
```

> [!TIP]
> **Por que precisamos do `linear_sum_assignment`?**  
> Como o K-Means não sabe português nem latim, ele pode chamar a flor *Setosa* de `Cluster 1`, enquanto o `LabelEncoder` chamou a *Setosa* de `0`. O mapeamento descobre qual número de cluster equivale a qual espécie antes de calcular a nota, revelando impressionantes **89,33% de acerto (134 de 150 flores)** sem supervisão!

---

## 5. 📐 O Segredo do $K$: Como definir o número ideal de Clusters?

Na vida real, quando recebemos uma base de dados desconhecida, **ninguém nos conta que existem 3 grupos ($K=3$)**. Como o Cientista de Dados descobre qual é o melhor valor de $K$? Utilizamos dois métodos matemáticos complementares:

### 🔹 A. Método do Cotovelo (*Elbow Method*)
Testamos vários valores de $K$ (de $1$ a $10$) e medimos a **Inércia** (`kmeans.inertia_`), que é a soma das distâncias quadradas das flores até o centro do seu grupo. Buscamos o ponto onde a curva dobra como um **"cotovelo"** — isto é, onde adicionar mais grupos deixa de trazer ganho real:

```python
inercias = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X)
    inercias.append(kmeans.inertia_)

plt.plot(range(1, 11), inercias, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia')
plt.title('Método do Cotovelo')
plt.show()
```

#### 📊 Saída Gráfica do Bloco 5A (Método do Cotovelo):
![Gráfico Método do Cotovelo](C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/iris_metodo_cotovelo.png)

> **Interpretando o Cotovelo:** Veja como a inércia despenca de `~681` ($k=1$) para `~152` ($k=2$) e chega a **`~78` em $k=3$**. A partir do **3**, a linha fica quase horizontal (formando a dobra do cotovelo no $k=3$). Isso comprova matematicamente que **$K=3$** é o ponto ótimo!

---

### 🔹 B. Índice de Silhueta (*Silhouette Score*)
Mede simultaneamente o quão **coeso** cada ponto está dentro do seu próprio cluster e o quão **separado** ele está dos outros clusters. Valores próximos de **`1.0`** indicam agrupamentos excelentes e bem definidos:

```python
from sklearn.metrics import silhouette_score

silhouette_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    silhouette_scores.append(score)

plt.plot(range(2, 11), silhouette_scores, marker='o', color='red')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Índice de Silhueta')
plt.title('Índice de Silhueta')
plt.show()
```

#### 📊 Saída Gráfica do Bloco 5B (Índice de Silhueta):
![Gráfico Índice de Silhueta](C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/iris_indice_silhueta.png)

> **Interpretando a Silhueta:**  
> * Em **$k=2$** o índice atinge `0.68` porque separar a ilha isolada da *Setosa* do bloco formado pelas outras duas espécies cria dois macrogrupos muito distantes entre si.  
> * Em **$k=3$** o índice mantém um patamar elevado (`0.55`), dividindo *Versicolor* e *Virginica*, e despenca rapidamente para $k \ge 4$ (`< 0.49`), provando que dividir em 4 ou mais grupos fragmenta artificialmente as espécies!

---

## 🏆 Conclusão do Laboratório

O **Aprendizado Não Supervisionado** é uma ferramenta indispensável para **exploração de dados e descoberta de padrões**. Neste laboratório:
1. Transformamos dados tabulares brutos em visualizações ricas (`scatterplot` e `pairplot`).
2. "Cegamos" os dados removendo a coluna `species` e aplicamos o algoritmo **K-Means**.
3. Identificamos automaticamente as **3 espécies da flor Iris com `89.33%` de precisão**, sem nunca "explicar" ao computador o que era uma *Setosa*, uma *Versicolor* ou uma *Virginica*!
4. Validamos matematicamente o número ideal de grupos combinando o **Método do Cotovelo** e o **Índice de Silhueta**.
