## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# SISTEMA COMPLETO DE ALPR (YOLOV8 + OPENCV + EASYOCR)
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

import cv2
import easyocr
from ultralytics import YOLO
from google.colab.patches import cv2_imshow

# 1. Carregamento dos modelos
detector = YOLO('yolov8s.pt')
ocr = easyocr.Reader(['en', 'pt'], gpu=True)

def processar_veiculo_alpr(caminho_foto):
    img = cv2.imread(caminho_foto)
    dets = detector(caminho_foto, conf=0.45)[0]
    
    for box in dets.boxes:
        if int(box.cls[0]) in [2, 3, 5, 7]:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # Recorte estratégico da metade inferior (onde fica a placa)
            altura_carro = y2 - y1
            y_placa_inicio = int(y1 + (altura_carro * 0.55))
            roi_placa = img[y_placa_inicio:y2, x1:x2]
            
            textos = ocr.readtext(roi_placa)
            for _, txt, conf in textos:
                limpo = "".join([c for c in txt if c.isalnum()]).upper()
                if len(limpo) >= 6 and conf >= 0.40:
                    print(f" Veículo Detectado! Placa: {limpo} (Confiança: {conf*100:.1f}%)")
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(img, f"PLACA: {limpo}", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2_imshow(img)

# Exemplo de chamada:
# processar_veiculo_alpr('carro_exemplo.jpg')
```
