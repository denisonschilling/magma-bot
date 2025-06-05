from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Preencha com suas credenciais da Z-API
TOKEN = 'SEU_TOKEN_AQUI'
ID_INSTANCIA = 'SUA_INSTANCIA_ID_AQUI'

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and 'message' in data:
        msg = data['message'].strip()
        telefone = data['phone']

        resposta = interpretar_mensagem(msg)
        enviar_resposta(telefone, resposta)
    return jsonify({'status': 'ok'})

def interpretar_mensagem(msg):
    if msg == "1":
        return "🔁 Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "📋 Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif msg == "3":
        return "🆘 Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
    else:
        return "Olá! Responda com:\n1️⃣ Renovar\n2️⃣ Cotar\n3️⃣ Assistência"

def enviar_resposta(telefone, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "phone": telefone,
        "message": texto
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def index():
    return "Bot da Magma X está online! 🔥", 200
