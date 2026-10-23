# flask_app.py - Servidor Web e Webhook de Integracao Dialogflow ES (Aula 05 - SENAI-SP)
# Projeto Oficial: DialogFlow.md (Pizzaria Inteligente IA-Pizza & Agendamento IA-Style)

from flask import Flask, request, jsonify, make_response, render_template_string

app = Flask(__name__)

# Lista global em memoria para persistir os pedidos recebidos em tempo real
pedidos = []

HTML_PAGE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pizzaria Inteligente IA-Pizza • SENAI-SP</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            color: #f8fafc;
            margin: 0;
            padding: 40px 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        .card {
            max-width: 650px;
            width: 100%;
            background: rgba(30, 41, 59, 0.85);
            border: 1px solid #334155;
            border-top: 5px solid #E30613;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            text-align: center;
        }
        h1 { color: #ffffff; margin-bottom: 8px; font-size: 28px; }
        h3 { color: #E30613; font-weight: 600; margin-top: 0; }
        p { color: #94a3b8; font-size: 15px; line-height: 1.6; }
        .badge {
            display: inline-block;
            background: #E30613;
            color: #fff;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 15px;
        }
        df-messenger {
            --df-messenger-bot-message: #334155;
            --df-messenger-button-titlebar-color: #E30613;
            --df-messenger-chat-background-color: #0f172a;
            --df-messenger-font-color: #ffffff;
            --df-messenger-send-icon: #E30613;
            --df-messenger-user-message: #E30613;
        }
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">Projeto Oficial DialogFlow.md</span>
        <h1>🍕 Pizzaria Inteligente IA-Pizza</h1>
        <h3>Atendimento Automatizado NLU + Deploy Cloud Flask</h3>
        <p>Utilize o balao de chat no canto inferior direito para fazer seu pedido de pizza em linguagem natural. A IA extraira sabor, tamanho, endereco e forma de pagamento automaticamente!</p>
    </div>

    <!-- Script Oficial do Google Dialogflow Messenger -->
    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="Pizzaria IA-Pizza"
      agent-id="SEU-AGENT-ID-AQUI"
      language-code="pt-br"
    ></df-messenger>
</body>
</html>'''

@app.route('/', methods=['GET'])
def home():
    """Rota principal GET: Exibe a pagina da Pizzaria com o Dialogflow Messenger"""
    return render_template_string(HTML_PAGE)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Rota POST do Webhook: Processa as Intencoes do Dialogflow em tempo real"""
    dados = request.get_json(silent=True, force=True) or {}
    query_result = dados.get('queryResult', {})
    intent_name = query_result.get('intent', {}).get('displayName', '')
    parametros = query_result.get('parameters', {})
    source = dados.get('originalDetectIntentRequest', {}).get('source', '')

    resposta = {"fulfillmentMessages": []}

    # 1. Intent Principal do DialogFlow.md: pedido.pizza
    if intent_name == 'pedido.pizza':
        sabor = parametros.get('sabor', 'Calabresa')
        tamanho = parametros.get('tamanho', 'Grande')
        pagamento = parametros.get('pagamento', 'PIX')
        endereco = parametros.get('endereco', 'Retirada no Balcao')

        registro = {
            "sabor": sabor,
            "tamanho": tamanho,
            "pagamento": pagamento,
            "endereco": endereco
        }
        pedidos.append(registro)

        msg = f"Pizza de {sabor} ({tamanho}) anotada com sucesso! Entrega em: {endereco}. Pagamento via {pagamento}."
        return enviar_cards("🍕 Pedido Registrado!", msg, source, resposta)

    # 2. Intent de Agendamento do DialogFlow.md: agendamento.servico
    elif intent_name == 'agendamento.servico':
        servico = parametros.get('servico', 'Corte de Cabelo')
        barbeiro = parametros.get('barbeiro', 'Ricardo')
        data_hora = parametros.get('data_hora', 'Hoje')

        msg = f"Agendamento confirmado: {servico} com o profissional {barbeiro} em {data_hora}!"
        return enviar_cards("✂️ Agendamento Confirmado!", msg, source, resposta)

    # 3. Intent de Consulta de Pedidos
    elif intent_name in ['Consultar_Status_Pedido', 'status.pedido']:
        msg = f"Temos {len(pedidos)} pedido(s) em preparo na cozinha neste momento. O ultimo pedido registrado foi: {pedidos[-1]['sabor'] if pedidos else 'Nenhum'}."
        return enviar_cards("📋 Status dos Pedidos", msg, source, resposta)

    # 4. Fallback padrao
    return jsonify({
        "fulfillmentText": "Recebi sua solicitacao no Webhook PythonAnywhere, mas nao reconheci a intencao cadastrada."
    })

def enviar_cards(titulo, msg, source, resposta):
    """Retorna Rich Content para o Dialogflow Messenger ou Card para o Console"""
    if source == 'DIALOGFLOW_CONSOLE' or source == 'telegram':
        resposta['fulfillmentMessages'].append({
            "card": {
                "title": titulo,
                "subtitle": msg
            }
        })
    else:
        # Formato Rich Content para o widget <df-messenger>
        resposta["fulfillmentMessages"].append({
            "payload": {
                "richContent": [[{
                    "type": "info",
                    "title": titulo,
                    "subtitle": msg
                }]]
            }
        })
    return make_response(jsonify(resposta))

if __name__ == '__main__':
    app.run(debug=True)
