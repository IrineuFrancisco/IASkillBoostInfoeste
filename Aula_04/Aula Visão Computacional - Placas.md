
# 🚗 Aula: Visão Computacional de Ponta a Ponta
## Detecção de Veículos e Reconhecimento de Placas (ALPR)

Nesta aula, vamos construir um sistema de **ALPR** (*Automatic License Plate Recognition*). Esse tipo de tecnologia é a base de sistemas de pedágio automático (Sem Parar), monitoramento de segurança urbana e controle de estacionamentos inteligentes.

---

### 1. A Arquitetura do Sistema
Antes do código, entenda o fluxo lógico. Não é apenas "um código que lê placas", mas uma **esteira de processamento (pipeline)**:

1.  **Detecção de Objeto (YOLOv8):** Localiza o veículo no espaço 2D da imagem.
2.  **Segmentação/Recorte (OpenCV):** Isola o veículo para reduzir o "ruído" (árvores, prédios) que atrapalharia o OCR.
3.  **Reconhecimento Óptico de Caracteres (EasyOCR):** Analisa os pixels do recorte em busca de padrões alfanuméricos.

---

### 2. Preparação do Ambiente e Modelos
Vamos carregar os "motores" de inteligência.

```python
!pip install -q easyocr ultralytics # O '-q' limpa as mensagens de instalação
import easyocr
from ultralytics import YOLO
import cv2
from google.colab.patches import cv2_imshow
from google.colab import files

# Inicialização dos Modelos
# O modelo 's' (small) é ideal para iniciantes: leve para o Colab, mas muito preciso.
detector_veiculos = YOLO('yolov8s.pt')
leitor_texto = easyocr.Reader(['en'], gpu=True) # Ativamos a GPU para maior velocidade
```

> **Nota Técnica:** O parâmetro `gpu=True` no EasyOCR faz com que o processamento seja feito na placa de vídeo do Google Colab, tornando a leitura até 10x mais rápida.

---

### 3. O Coração do Código: Detecção e Inteligência
Aqui, vamos iterar sobre as detecções e aplicar filtros inteligentes para evitar falsos positivos.

```python
# 1. Upload da imagem
uploaded = files.upload()
nome_arquivo = list(uploaded.keys())[0]
imagem_original = cv2.imread(nome_arquivo)

# 2. Execução da IA de Detecção
# Definimos as classes de interesse: 2 (carro), 3 (moto), 5 (ônibus), 7 (caminhão)
classes_veiculos = [2, 3, 5, 7]
resultados = detector_veiculos.predict(nome_arquivo, conf=0.5)

# 3. Loop de Processamento por Veículo Encontrado
for objeto in resultados[0].boxes:
    classe_id = int(objeto.cls[0])
    
    if classe_id in classes_veiculos:
        # Extração de Coordenadas (Bounding Box)
        x1, y1, x2, y2 = map(int, objeto.xyxy[0])
        
        # Recorte Estratégico (ROI - Region of Interest)
        # Cortamos a área do veículo com uma pequena margem
        recorte_veiculo = imagem_original[y1:y2, x1:x2]
        
        # Execução do OCR no recorte
        resultado_ocr = leitor_texto.readtext(recorte_veiculo)
        
        # Exibição dos resultados válidos
        for (bbox, texto, confiança) in resultado_ocr:
            texto_limpo = texto.replace(" ", "").upper() # Remove espaços e padroniza
            
            # Filtro de Placa: Placas brasileiras têm entre 7 e 8 caracteres (com hífen)
            if len(texto_limpo) >= 5:
                print(f"✅ VEÍCULO DETECTADO: {detector_veiculos.names[classe_id]}")
                print(f"📝 TEXTO DA PLACA: {texto_limpo} (Confiança: {confiança:.2%})")
                cv2_imshow(recorte_veiculo)
                print("-" * 30)
```

---

### 4. Por que isso funciona? (Explicação de Conceitos)

* **Matrizes de Pixels:** Para o computador, a imagem é uma tabela de números. Quando fazemos `imagem[y1:y2, x1:x2]`, estamos selecionando um subconjunto dessa tabela.
* **Limiar de Confiança (`conf`):** É o filtro de "certeza" da IA. Se for muito baixo (0.1), ela verá carros em sombras. Se for muito alto (0.9), ela pode ignorar carros distantes.
* **Padrão COCO:** O YOLO vem treinado no dataset COCO, que possui 80 classes. Conhecer os IDs (2, 3, 5, 7) é essencial para filtrar o que não nos interessa.

---

### 5. Desafio de Aperfeiçoamento (Exercícios)

Para fixar o aprendizado, tente realizar as seguintes modificações:

1.  **Otimização Visual:** Altere o código para desenhar um retângulo verde ao redor da placa diretamente na imagem original usando a função `cv2.rectangle`.
2.  **Lógica de Negócio:** Crie uma lista chamada `lista_negra = ["ABC1234", "XYZ9876"]`. Se o OCR ler uma placa que esteja nessa lista, exiba um alerta: **"⚠️ VEÍCULO ROUBADO DETECTADO!"**.
3.  **Filtro de Ruído:** Placas Mercosul seguem o padrão `AAA0A00`. Tente usar uma biblioteca chamada `re` (Expressões Regulares) para validar se o texto lido realmente parece uma placa de carro.

---

<!-- **Dica para o professor:**
> Se os alunos tiverem dificuldade em ler placas muito pequenas, sugira que eles usem o modelo `yolov8l.pt` (large), que é mais pesado, mas detecta objetos menores com mais facilidade.

---
**Gostaria que eu gerasse um exemplo de como aplicar o filtro de Expressões Regulares (Regex) para validar as placas Mercosul?** -->