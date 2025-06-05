from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Credenciais da Z-API
TOKEN = '56100423CA70A6B650E3638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 DADOS RECEBIDOS:", data)

    msg = data.get('message') or data.get('mensagem') or data.get('text', {}).get('body')
    telefone = data.get('phone') or data.get('telefone')

    resposta = interpretar_mensagem(msg)
    enviar_resposta(telefone, resposta)

    return jsonify({'status': 'OK'})

def interpretar_mensagem(msg):
    if msg == "1":
        return "✅ OK! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "🟢 Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif msg == "3":
        return "🚨 Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
    else:
        return "Olá! Responda com:\n🔁 Renovar\n🆕 Cotar\n🆘 Assistência"

def enviar_resposta(telefone, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "phone": telefone,
        "message": texto
    }

    print("📤 ENVIANDO PARA API:", url)
    print("📦 PAYLOAD:", payload)

    response = requests.post(url, json=payload)
    print("📬 RESPOSTA DA API:", response.status_code, response.text)

@app.route("/status", methods=["GET"])
def status():
    return "✅ Bot da Magma X está online!", 200
