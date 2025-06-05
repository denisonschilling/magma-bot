from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# ✅ Credenciais da Z-API
TOKEN = '56100423CA70A6B650E3638D'
ID_INSTANCIA = '3E23640FFCACE0DC14473274D0A2B459'

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📦 DADOS COMPLETOS:", json.dumps(data, indent=2, ensure_ascii=False))

    # ⛔ Ignorar mensagens de grupo
    if data.get('isGroup') or data.get('grupo') is True:
        print("🚫 Mensagem ignorada: veio de grupo.")
        return jsonify({"status": "ignorado - grupo"})

    # ✅ Extrair mensagem
    msg = (
        data.get('message') or
        data.get('mensagem') or
        data.get('text', {}).get('body') or
        data.get('text') or
        data.get('payload', {}).get('text') or
        data.get('payload', {}).get('message') or
        ""
    )

    # ✅ Extrair telefone
    telefone = (
        data.get('phone') or
        data.get('telefone') or
        data.get('sender', {}).get('phone') or
        data.get('payload', {}).get('sender', {}).get('phone') or
        ""
    )

    # ✅ Enviar resposta
    if msg and telefone:
        resposta = interpretar_mensagem(msg.strip())
        enviar_resposta(telefone, resposta)
    else:
        print("❌ ERRO: Mensagem ou telefone não foram encontrados!")

    return jsonify({"status": "ok"})

def interpretar_mensagem(msg):
    if msg == "1":
        return "✅ Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "✅ Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif msg == "3":
        return "🚨 Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
    else:
        return "📋 Opções:\n1️⃣ Renovar\n2️⃣ Cotar\n3️⃣ Assistência"

def enviar_resposta(telefone, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "phone": telefone,
        "message": texto
    }

    print("📤 ENVIANDO PARA API:", url)
    print("📦 PAYLOAD:", payload)

    response = requests.post(url, json=payload)
    print("📨 RESPOSTA DA API:", response.status_code, response.text)

@app.route("/status", methods=["GET"])
def status():
    return "✅ Bot da Magma X está online!", 200
