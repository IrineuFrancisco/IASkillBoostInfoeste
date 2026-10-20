

# Passo a Passo: Integração Cantina SENAI (Dialogflow + PythonAnywhere)

## 1. Configuração no Dialogflow (O Cérebro)

### 1.1. Criar Entidade de Produto
1. Vá em **Entities** > **Create Entity**.
2. Nome: `produto`.
3. Valores: `coxinha de frango`, `coxinha de costela`. (Adicione sinônimos se desejar).
4. Clique em **Save**.

### 1.2. Criar a Intent de Pedido
1. Vá em **Intents** > **Create Intent**.
2. Nome da Intent: **`pedido-coxinha`** (O nome deve ser exatamente este para o código funcionar).
3. Em **Training Phrases**, adicione exemplos:
   - *"Quero 2 coxinhas de frango"*
   - *"Vou querer 5 de costela"*
4. Na seção **Action and Parameters**, verifique se o Dialogflow identificou:
   - Parâmetro: `qtde` (Entity: `@sys.number`)
   - Parâmetro: `produto` (Entity: `@produto`)
5. Marque ambos como **REQUIRED** (Obrigatório).
6. No final da página, em **Fulfillment**, clique em **Enable Fulfillment** e ative:
   - **Enable webhook call for this intent**.
7. Clique em **Save**.

---

## 2. Configuração no PythonAnywhere (O Servidor)

### 2.1. Criar o Web App
1. Acesse o [PythonAnywhere](https://www.pythonanywhere.com/).
2. Vá na aba **Web** > **Add a new web app**.
3. Escolha **Flask** e a versão mais recente do **Python (Ex: 3.10)**.

### 2.2. Organizar Arquivos e Imagem
1. Vá na aba **Files**.
2. Crie uma pasta chamada `static` dentro do seu diretório principal.
3. Dentro de `static`, crie uma pasta chamada `images`.
4. Faça o upload de um ícone de robô chamado `robot.png` dentro de `/static/images/`.

### 2.3. Implementar o Código
Abra o arquivo `flask_app.py` e cole o código abaixo (uma versão limpa e organizada do seu código):

```python
from flask import Flask, url_for, make_response, request, jsonify

app = Flask(__name__)

pedidos = []

@app.route('/', methods=["GET"])
def website():
    # OBS: Substitua o agent-id pelo seu ID do Dialogflow
    return """
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            df-messenger {
                --df-messenger-bot-message: #b3a89d;
                --df-messenger-button-titlebar-color: #ededed;
                --df-messenger-chat-background-color: #c7c7c7;
                --df-messenger-font-color: white;
                --df-messenger-send-icon: #c7c7c7;
                --df-messenger-user-message: #9db3b0;
            }
        </style>
    </head>
    <body>
    <p><h2>Cantina</h2></p>
    <p><h4>SENAI 9.14 - Presidente Prudente - SP</h4></p>
    <p><h4>Professor: Anderson Roberto de Aguiar</h4></p>

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
        intent="WELCOME"
        chat-title="SENAIBOT"
        agent-id="1ae8127a-34d0-4866-88f3-b523b9060b73" 
        language-code="pt-br"
        chat-icon='%s'>
    </df-messenger>
    </body>
    </html>
    """ % url_for('static', filename='images/robot.png')

@app.route('/webhook', methods=["POST"])
def processarIntent():
    payload = request.get_json()
    intent = payload.get('queryResult').get('intent')
    
    if intent:
        if intent.get('displayName') == 'pedido-coxinha':
            # Identifica a origem (Console do Dialogflow ou Web Messenger)
            source = payload.get("originalDetectIntentRequest", {}).get("source")
            resposta = {"fulfillmentMessages": []}
            
            parametro = payload.get('queryResult').get('parameters')
            qtde = parametro.get("qtde")
            prod = parametro.get("produto")

            # Salva na lista global de pedidos
            dict_prod = {"produto": prod, "qtde": qtde}
            global pedidos
            pedidos.append(dict_prod)

            msg = f"Ok, seu pedido de {qtde} {prod} foi realizado com sucesso!"
            return enviarCards(msg, source, resposta)
    
    return make_response(jsonify({"fulfillmentText": "Intent não reconhecida pelo Webhook."}))

def enviarCards(msg, source, resposta):
    if source == "DIALOGFLOW_CONSOLE" or source == "telegram":
        cardMsg = obterCardMsg(msg, tipo='custom')
        for card in cardMsg:
            resposta['fulfillmentMessages'].append(card)
    else:
        # Formato para Dialogflow Messenger (Rich Content)
        cardMsg = obterCardMsg(msg, tipo='messenger')
        resposta["fulfillmentMessages"].append({
            "payload": {
                "richContent": [cardMsg]
            }
        })
    return make_response(jsonify(resposta))

def obterCardMsg(msg, tipo="custom"):
    if tipo == "custom":
        return [{
            "card": {
                "title": "Mensagem de Confirmação",
                "subtitle": msg,
                "buttons": [
                    {"text": "Sair", "postback": "sair"}
                ]
            }
        }]
    elif tipo == "messenger":
        return [{
            "type": "info",
            "title": "Confirmação de Pedido",
            "subtitle": msg,
            "image": {"src": {"rawUrl": ""}},
            "actionLink": ""
        }]

if __name__ == '__main__':
    app.run()
```

---

## 3. Vinculando as Pontas (Fulfillment)

1. No **PythonAnywhere**, na aba **Web**, clique no botão verde **Reload**.
2. Copie a URL do seu site (Ex: `https://seuusuario.pythonanywhere.com/webhook`).
3. No **Dialogflow**, vá em **Fulfillment**.
4. Ative o **Webhook**.
5. No campo **URL**, cole o endereço que você copiou (certifique-se de que termine com `/webhook`).
6. Clique em **Save**.

---

## 4. Como testar

1. **Pelo Console do Dialogflow:** Digite "Quero 3 coxinhas de frango". O bot deve responder com o Card de sistema (Custom Card).
2. **Pela Página Web:** Acesse `https://seuusuario.pythonanywhere.com/`. O chat aparecerá no canto inferior direito. Ao fazer o pedido, ele exibirá o `info card` do Messenger (Rich Content).

---

### Dicas para o NotebookLM (Infográfico):
Você pode pedir ao NotebookLM para:
1. *"Explique como a função `enviarCards` diferencia um acesso via Telegram de um acesso via Site."*
2. *"Descreva o papel da lista global `pedidos` no código Python."*
3. *"Crie um esquema visual da rota `/` mostrando como ela carrega o chat do Dialogflow."*