## 💻 CÓDIGO FONTE FINAL COMPLETO (EXECUTÁVEL NO GOOGLE COLAB)

```python
# ==============================================================================
# PIPELINE HÍBRIDO ML + GENAI (RANDOM FOREST + GEMINI 1.5 FLASH)
# SENAI-SP & Infoeste — Trilha Google Cloud Skills Boost
# ==============================================================================

import pandas as pd
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import google.generativeai as genai

# 1. Carga dos dados
df = pd.read_csv('ecommerce_clientes.csv')
features = ['tempo_no_site_minutos', 'paginas_visitadas', 'itens_no_carrinho', 'dias_sem_comprar', 'valor_carrinho_reais']

X = df[features]
y = df['abandonou_carrinho']

# 2. Treino do Classificador Random Forest
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

print(f"Modelo de Churn Treinado com Acurácia de: {rf.score(X_test, y_test)*100:.1f}%\n")

# 3. Configuração do Gemini API
API_KEY = "SUA_CHAVE_AQUI"
genai.configure(api_key=API_KEY)
gemini = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature": 0.5, "response_mime_type": "application/json"}
)

# 4. Função de Predição e Resgate
def pipeline_resgate(cliente):
    df_c = pd.DataFrame([cliente])
    prob = rf.predict_proba(df_c)[0][1]
    print(f"Risco de Abandono: {prob*100:.1f}%")
    
    if prob >= 0.70:
        prompt = f"""
        Gere um cupom de desconto em formato JSON para o cliente com carrinho de R$ {cliente['valor_carrinho_reais']:.2f}.
        Campos: "cupom", "desconto_pct", "mensagem".
        """
        res = gemini.generate_content(prompt)
        return json.loads(res.text)
    return {"status": "baixo_risco"}

# Exemplo de teste
cliente_teste = {'tempo_no_site_minutos': 2.0, 'paginas_visitadas': 1, 'itens_no_carrinho': 3, 'dias_sem_comprar': 30, 'valor_carrinho_reais': 250.0}
print(pipeline_resgate(cliente_teste))
```
