from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Z-API config
TOKEN = '56100423CA70A6B6503E638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
ZAPI_URL = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text'

def enviar_resposta(chat_id, texto):
    payload = {
        "chatId": chat_id,
        "message": texto
    }
    try:
        print(f"➡️ Enviando para {chat_id}: {texto}")
        response = requests.post(ZAPI_URL, json=payload)
        print("📨 Resposta:", response.status_code, response.text)
    except Exception as e:
        print("❌ ERRO ao enviar:", str(e))

def interpretar_mensagem(msg):
    msg = msg.strip().lower()
    if msg == "1":
        return "🟢 Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "📋 Certo! Vamos cotar um novo seguro. Me diga o tipo (auto, residencial, etc)."
    elif msg == "3":
        return "🛠️ Assistência 24h? Me diga sua localização ou endereço."
    else:
        return "📋 Opções:\n1️⃣ Renovar\n2️⃣ Cotar\n3️⃣ Assistência"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 RECEBIDO:", json.dumps(data, indent=2, ensure_ascii=False))

    # Detecta a mensagem de qualquer forma possível
    msg = (
        data.get('mensagem') or
        data.get('message') or
        data.get('text', {}).get('body') or
        data.get('text') or
        ""
    )

    # Detecta o telefone ou chatId
    telefone = (
        data.get('phone') or
        data.get('sender', {}).get('phone') or
        data.get('chatId') or
        ""
    )

    chat_id = telefone if "@c.us" in telefone else f"{telefone}@c.us" if telefone else ""

    if not msg or not chat_id:
        print("❌ ERRO: mensagem ou telefone ausentes.")
        return jsonify({"erro": "dados insuficientes"}), 400

    resposta = interpretar_mensagem(msg)
    enviar_resposta(chat_id, resposta)

    return jsonify({"status": "mensagem enviada"}), 200

@app.route("/status", methods=["GET"])
def
