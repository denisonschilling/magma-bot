from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Preencha com suas credenciais da Z-API
TOKEN = '56100423CA70A6B650E3638D'
ID_INSTANCIA = '3E23640FFCACE0DC14473274D0A2B459'

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 DADOS RECEBIDOS:", data)

    if data and ('message' in data or 'mensagem' in data):
        msg = data.get('message') or data.get('mensagem')
        telefone = data.get('phone') or data.get('telefone')

        resposta = interpretar_mensagem(msg)
        enviar_resposta(telefone, resposta)

    return jsonify({'status': 'OK'})

def interpretar_mensagem(mensagem):
    if mensagem == "1":
        return "🔁 Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif mensagem == "2":
        return "📋 Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif mensagem == "3":
        return "🛠️ Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
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
    return "🤖 Bot da Magma X está online!", 200


@app.route("/", methods=["GET"])
def index():
    return "🤖 Bot da Magma X está online!", 200
