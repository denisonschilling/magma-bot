from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Preencha com suas credenciais da Z-API
TOKEN = '56100423CA70A6B650E3638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 DADOS RECEBIDOS:", data)

    if data and ('mensagem' in data or 'message' in data):
        msg = data.get('mensagem') or data.get('message')
        telefone = data.get('telefone') or data.get('phone')

        resposta = interpretar_mensagem(msg)
        enviar_resposta(telefone, resposta)

    return jsonify({'status': 'OK'})

def interpretar_mensagem(msg):
    if msg == "1":
        return "🔁 Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "✅ Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif msg == "3":
        return "🚨 Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
    else:
        return "Olá! Responda com:\n1️⃣ Renovar\n2️⃣ Cotar\n3️⃣ Assistência"

def enviar_resposta(telefone, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "phone": telefone,
        "message": texto
    }
    requests.post(url, json=payload)

@app.route("/status", methods=["GET"])
def status():
    return "🟢 Bot da Magma X está online!", 200
