## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# PIPELINE COMPLETO DE DETECÇÃO E CONTAGEM (ULTRALYTICS YOLOV8)
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

from ultralytics import YOLO
from collections import Counter
from google.colab.patches import cv2_imshow

def auditar_imagem_yolo(caminho_imagem, threshold=0.5):
    yolo = YOLO('yolov8s.pt')
    res = yolo.predict(caminho_imagem, conf=threshold)[0]
    
    classes = [res.names[int(b.cls[0])] for b in res.boxes]
    contagem = Counter(classes)
    
    print(f"=== INVENTÁRIO DO ARMAZÉM ({caminho_imagem}) ===")
    for k, v in contagem.items():
        print(f"  • {k.capitalize()}: {v}")
        
    cv2_imshow(res.plot())

# Exemplo de chamada:
# auditar_imagem_yolo('sua_foto.jpg', threshold=0.5)
```
