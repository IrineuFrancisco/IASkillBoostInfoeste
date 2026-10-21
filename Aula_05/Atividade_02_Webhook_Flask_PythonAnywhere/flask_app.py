# flask_app.py - Servidor Web e Webhook de Integracao Dialogflow ES (Aula 05 - SENAI-SP)
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML_PAGE = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Portal de Atendimento IA - SENAI</title>
    <style>
        body { font-family: Arial, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; }
        .card { max-width: 700px; margin: 0 auto; background: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #38bdf8; }
        h1 { color: #38bdf8; }
        df-messenger {
            --df-messenger-bot-message: #1e293b;
            --df-messenger-button-titlebar-color: #2563eb;
            --df-messenger-chat-background-color: #0f172a;
            --df-messenger-font-color: #ffffff;
            --df-messenger-send-icon: #38bdf8;
            --df-messenger-user-message: #2563eb;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>Central de Atendimento Inteligente</h1>
        <p>Utilize o icone de chat no canto inferior direito para conversar com nosso Agente Virtual integrado ao Dialogflow e PythonAnywhere.</p>
    </div>

    <script src="https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1"></script>
    <df-messenger
      intent="WELCOME"
      chat-title="Assistente_SENAI"
      agent-id="SEU-AGENT-ID-AQUI"
      language-code="pt-br"
    ></df-messenger>
</body>
</html>'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/webhook', methods=['POST'])
def webhook():
    dados = request.get_json(silent=True, force=True)
    intent_name = dados.get('queryResult', {}).get('intent', {}).get('displayName', '')
    parametros = dados.get('queryResult', {}).get('parameters', {})

    if intent_name == 'Consultar_Status_Pedido':
        numero_pedido = parametros.get('numero_pedido', '0000')
        resposta = f"Consultei nosso banco de dados em nuvem: O pedido #{numero_pedido} ja saiu para entrega e chega hoje ate as 18h!"
    elif intent_name == 'Agendar_Suporte_Tecnico':
        horario = parametros.get('horario', '14:00')
        resposta = f"Perfeito! Seu atendimento tecnico foi registrado no servidor Python para as {horario}."
    else:
        resposta = "Recebi sua solicitacao no Webhook PythonAnywhere, mas nao reconheci a intencao."

    return jsonify({"fulfillmentText": resposta})

if __name__ == '__main__':
    app.run(debug=True)
