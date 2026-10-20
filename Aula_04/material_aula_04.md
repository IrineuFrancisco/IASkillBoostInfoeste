# 📘 Material Didático — Aula 04 (Dia 04): Visão Computacional (`YOLOv8`, `EasyOCR`, `DeepFace`), Ética e Trilha 03 (Skills Boost)
**Curso:** Aperfeiçoamento Profissional — Programação em Inteligência Artificial Generativa (SENAI-SP)  
**Carga Horária da Aula:** 4 Horas (Dia 4 de 5)  
**Apresentação de Slides:** [slides_aula_4_estudante.html](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/slides_aula_4_estudante.html)

---

## 🎯 Objetivos da Aula 04
1. Compreender como os computadores processam dados visuais em **matrizes de pixels (`OpenCV`)** e a diferença entre **Classificação de Imagens**, **Detecção de Objetos (`YOLOv8`)** e **Reconhecimento Facial (`DeepFace`)**.
2. Implementar no Google Colab o **Laboratório 4.1: Detecção e Contagem Automática de Objetos com `YOLOv8`** em imagens reais, minerando o objeto `boxes` com `Counter`.
3. Implementar o **Laboratório 4.2: Sistema de Leitura Automática de Placas Veiculares (ALPR)** unindo `YOLOv8` + fatiamento de Região de Interesse (`ROI`) no `OpenCV` + `EasyOCR`.
4. Implementar o **Laboratório 4.3: Reconhecimento de Emoções e Demografia Facial com `DeepFace`**.
5. Analisar os riscos éticos da Visão Computacional (Viés Algorítmico, Falsos Positivos, Privacidade/LGPD) e concluir a **Atividade 03 (*Introduction to Responsible AI*)** no **Google Cloud Skills Boost** (75% da trilha).

---

## 👁️ Módulo 1: Fundamentos de Visão Computacional

### 1.1 Classificação vs. Detecção vs. Reconhecimento Facial

```mermaid
flowchart LR
    subgraph T1 ["1. Classificação"]
        C1["Imagem Inteira"] --> C2["Rótulo Único\n('Isto é um Carro')"]
    end
    subgraph T2 ["2. Detecção de Objetos (YOLOv8)"]
        D1["Imagem ou Vídeo"] --> D2["O quê? + Onde?\nBounding Box [x1,y1,x2,y2] + Confiança"]
    end
    subgraph T3 ["3. Análise Facial (DeepFace)"]
        F1["Detecção + Alinhamento"] --> F2["Landmarks (68 pontos)\nEmoção / Idade / Identidade"]
    end
```

- **Bounding Box (Caixa Delimitadora):** Retângulo de coordenadas `(x1, y1, x2, y2)` desenhado ao redor de cada objeto detectado.
- **Confidence Score (Nível de Confiança):** Probabilidade entre `0.0` e `1.0` (`0%` a `100%`) que indica a certeza matemática da rede neural sobre a classe detectada.
- **Dataset COCO:** Base padrão na qual o **YOLOv8** é pré-treinado, contendo **80 classes de objetos** (`0: person`, `1: bicycle`, `2: car`, `3: motorcycle`, `5: bus`, `7: truck`, `16: dog`, etc.).

---

## 🚀 Módulo 2 (Laboratório 4.1): Detecção e Contagem de Objetos com `YOLOv8`

Siga os blocos abaixo no Google Colab (`Aula04_Lab1_Deteccao_YOLOv8.ipynb`):

### Passo 1 a 5: Instalação, Upload e Detecção Visual

```python
# PASSO 1: Instalação da biblioteca oficial Ultralytics
!pip install ultralytics --quiet

from ultralytics import YOLO
from google.colab import files
from google.colab.patches import cv2_imshow
from collections import Counter

# PASSO 2: Entrada de Dados (Upload de foto do seu computador)
print("Selecione uma imagem (jpg, png) para a IA analisar:")
uploaded = files.upload()
nome_do_arquivo = list(uploaded.keys())[0]

# PASSO 3 e 4: Carregamento do modelo YOLOv8 Small e Predição
modelo = YOLO('yolov8s.pt')
MINIMA_CONFIANCA = 0.5  # 50% de certeza mínima
resultados = modelo.predict(source=nome_do_arquivo, conf=MINIMA_CONFIANCA)

# PASSO 5: Visualização Amigável com Bounding Boxes
resultado_renderizado = resultados[0].plot(line_width=2, font_size=12)
print("\n--- Resultado Visual ---")
cv2_imshow(resultado_renderizado)
```

**Saída do Console (Passos 1 a 5):**
```text
Saving dog bike.jpg to dog bike.jpg
image 1/1 /content/dog bike.jpg: 480x640 1 bicycle, 1 truck, 1 dog, 491.8ms
Speed: 6.0ms preprocess, 491.8ms inference, 1.4ms postprocess per image at shape (1, 3, 480, 640)
```

![Saída Visual do Lab 4.1: Detecção YOLOv8](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/yolo_obj_out_1.png)

---

### Passo 6: Extração Estruturada de Dados e Relatório Estatístico

```python
print("\n--- RELATÓRIO DETALHADO ---")
objetos_nomes = []

# Iterar sobre cada 'box' (caixa delimitadora) detectada pela IA
for box in resultados[0].boxes:
    id_classe = int(box.cls[0])           # ID numérico no dataset COCO
    nome = resultados[0].names[id_classe] # Nome textual (ex: 'dog')
    conf = float(box.conf[0])             # Nível de certeza (0 a 1)
    
    objetos_nomes.append(nome)
    print(f"✅ Encontrado: {nome.upper()} | Confiança: {conf:.2%}")

# Resumo estatístico com Counter
contagem = Counter(objetos_nomes)
print("\n--- RESUMO DA CONTAGEM ---")
for obj, qtd in contagem.items():
    print(f"• {obj.capitalize()}: {qtd}")
```

**Saída do Console (Passo 6):**
```text
--- RELATÓRIO DETALHADO ---
✅ Encontrado: DOG | Confiança: 92.72%
✅ Encontrado: BICYCLE | Confiança: 88.27%
✅ Encontrado: TRUCK | Confiança: 77.63%

--- RESUMO DA CONTAGEM ---
• Dog: 1
• Bicycle: 1
• Truck: 1
```

---

## 🚗 Módulo 3 (Laboratório 4.2): Monitoramento Inteligente e Leitura de Placas (ALPR)

Neste segundo laboratório, construiremos uma **esteira de processamento (*pipeline* ALPR)** usada em pedágios automáticos e estacionamentos inteligentes:
1. **Detecção (`YOLOv8`):** Localiza veículos (`classes [2, 3, 5, 7]`) no espaço 2D da foto.
2. **Recorte Estratégico (`OpenCV ROI`):** Fatiamento da matriz `imagem[y1:y2, x1:x2]` para isolar o veículo e eliminar ruídos de fundo.
3. **Reconhecimento Óptico de Caracteres (`EasyOCR`):** Lê os caracteres alfanuméricos da placa dentro do recorte.

### Bloco 1: Instalação e Inicialização dos Modelos

```python
!pip install -q easyocr ultralytics opencv-python

import easyocr
from ultralytics import YOLO
import cv2
from google.colab import files
from google.colab.patches import cv2_imshow

# Inicializa o leitor OCR para caracteres latinos e o YOLOv8 Small
reader = easyocr.Reader(['en'], gpu=True)
modelo = YOLO('yolov8s.pt')
```

---

### Bloco 2: Upload da Imagem e Visão do `YOLOv8`

```python
print("Selecione a imagem com carros com placas:")
uploaded = files.upload()
foto = list(uploaded.keys())[0]

imagem = cv2.imread(foto)
print("\nENTRADA: Imagem Original")
cv2_imshow(imagem)

# Realiza a detecção com confiança mínima de 40%
resultados = modelo.predict(foto, conf=0.4)

# Exibe as caixas delimitadoras encontradas pelo YOLOv8
img_ia = resultados[0].plot()
print("\nSAÍDA: O que a IA enxerga")
cv2_imshow(img_ia)
```

````carousel
![Entrada: Imagem Original do Veículo](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/yolo_placa_out_1.png)
<!-- slide -->
![Saída YOLOv8: 2 Carros Detectados (0.88 e 0.62)](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/yolo_placa_out_2.png)
````

---

### Bloco 3: Recorte da Região de Interesse (`ROI`) e Leitura da Placa (`EasyOCR`)

```python
print("\n--- RESULTADO DA LEITURA ---")

for res in resultados[0].boxes:
    # Filtro COCO: Classe 2 (Carro), 3 (Moto), 5 (Ônibus) ou 7 (Caminhão)
    if int(res.cls[0]) in [2, 3, 5, 7]:
        x1, y1, x2, y2 = map(int, res.xyxy[0])
        
        # Recorte da imagem usando fatiamento de matrizes (OpenCV)
        carro_recortado = cv2.imread(foto)[y1:y2, x1:x2]
        print("\nRecorte do Veículo:")
        cv2_imshow(carro_recortado)

        # O EasyOCR processa o recorte em busca de texto
        leitura = reader.readtext(carro_recortado)

        if leitura:
            for (bbox, texto, conf) in leitura:
                texto_limpo = texto.replace(" ", "").upper()
                if len(texto_limpo) >= 4:
                    print(f"📌 Possível Placa Detectada: {texto_limpo} (Confiança: {conf:.2%})")
        else:
            print("❌ Nenhuma placa encontrada")
```

````carousel
![Recorte 1: Renault Sandero (Placa OZU5J50)](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/yolo_placa_out_3.png)
<!-- slide -->
![Recorte 2: Segundo Carro Lateral (Sem Placa Visível)](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/yolo_placa_out_4.png)
````

**Saída Real do Console (Bloco 3):**
```text
--- RESULTADO DA LEITURA ---

Recorte do Veículo [1]:
📌 Possível Placa Detectada: 442IR8 (Confiança: 9.24%)
📌 Possível Placa Detectada: 0ZU5550 (Confiança: 31.40%)

Recorte do Veículo [2]:
❌ Nenhuma placa encontrada
```

> [!TIP]
> **Considerações Técnicas sobre o Retorno do OCR:**  
> 1. No **Recorte 1**, o EasyOCR leu tanto o emblema cromado `"SANDERO"` (interpretado com baixa confiança `9.24%` como `442IR8`) quanto a placa Mercosul `OZU5J50` (lida como `0ZU5550`, trocando `O` por `0` e `J` por `5`).  
> 2. No **Recorte 2**, como o segundo veículo aparece apenas de perfil (porta lateral branca), o loop retorna `❌ Nenhuma placa encontrada`.  
> 3. **Desafio de Aperfeiçoamento:** Adicione uma validação com Expressões Regulares (`import re`, padrão `^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$`) e uma `lista_negra = ["OZU5J50", "0ZU5550"]` para disparar um alerta de veículo procurado!

---

## 😊 Módulo 4 (Laboratório 4.3): Reconhecimento de Emoções Faciais com `DeepFace`

![Infográfico Completo: Reconhecimento de Emoções com DeepFace](file:///C:/Users/Instrutor/.gemini/antigravity/brain/2def7d10-b738-49f5-8f6f-980678220051/info_emocoes_deepface.png)

### Passo 1 e 2: Instalação e Algoritmo de Análise Facial

```python
# Passo 1: Instalação do framework DeepFace
!pip install deepface tf-keras --quiet
print("Ambiente configurado com sucesso!")

# Passo 2: Importação e Algoritmo de Análise
import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
from google.colab import files

def analisar_emocao_na_foto():
    uploaded = files.upload()
    img_path = list(uploaded.keys())[0]

    # Analisa as microexpressões faciais (emoções)
    resultados = DeepFace.analyze(img_path, actions=['emotion'])

    # Carrega a imagem e converte de BGR (OpenCV) para RGB (Matplotlib)
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    for face in resultados:
        x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
        emocao = face['dominant_emotion']
        
        # Desenha retângulo verde e escreve a emoção dominante
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 10)
        cv2.putText(img, emocao, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

    plt.imshow(img)
    plt.axis('off')
    plt.show()

analisar_emocao_na_foto()
```

---

## ⚖️ Módulo 5: Ética em IA e Atividade 03 da Trilha Google Cloud Skills Boost

Acesse a plataforma **Google Cloud Skills Boost** e conclua a **Atividade 03** da trilha *Iniciante: programa de aprendizado Introdução à IA generativa*:

- **Curso:** *Introduction to Responsible AI* (~30 minutos)
- **Conteúdo:** Os **7 Princípios de IA do Google**, mitigação de viés algorítmico, segurança, privacidade, transparência e aplicações que o Google se compromete a não desenvolver.

> [!WARNING]
> **REGRA OBRIGATÓRIA PARA O 3º BADGE:**  
> **Assista ao vídeo completo até o final** antes de responder ao Quiz! Ao concluir esta etapa, você alcança **75% da trilha oficial Google Cloud Skills Boost**.
