from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# 🔐 Credenciais da Z-API
TOKEN = '56100423CA70A6B6503E638D'
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 DADOS COMPLETOS:", json.dumps(data, indent=2, ensure_ascii=False))

    # ❌ Ignorar mensagens de grupo
    if data.get('isGroup') or data.get('grupo') is True:
        print("🚫 Mensagem ignorada: veio de grupo.")
        return jsonify({"status": "ignorado - grupo"})

    # 📤 Extrair mensagem
    msg = (
        data.get('message') or
        data.get('mensagem') or
        data.get('text', {}).get('body') or
        data.get('text') or
        data.get('payload', {}).get('text') or
        data.get('payload', {}).get('message') or
        ""
    )

    # 📞 Extrair número e formatar chatId
    telefone = (
        data.get('phone') or
        data.get('telefone') or
        data.get('sender', {}).get('phone') or
        data.get('payload', {}).get('sender', {}).get('phone') or
        ""
    )
    chat_id = f"{telefone}@c.us" if telefone else ""

    if msg and chat_id:
        resposta = interpretar_mensagem(msg.strip())
        enviar_resposta(chat_id, resposta)
    else:
        print("❌ ERRO: Mensagem ou telefone não encontrados!")
    
    return jsonify({"status": "ok"})

# 🤖 Função para interpretar mensagem recebida
def interpretar_mensagem(msg):
    if msg == "1":
        return "🟢 Ok! Vamos renovar seu seguro. Me diga seu CPF."
    elif msg == "2":
        return "🟢 Certo! Vamos cotar um novo seguro. Me diga o tipo: auto, residencial, etc."
    elif msg == "3":
        return "🛠️ Assistência 24h? Já estou encaminhando. Me diga seu endereço ou localização."
    else:
        return "📋 Opções:\n1️⃣ Renovar\n2️⃣ Cotar\n3️⃣ Assistência"

# 📤 Envio de resposta para API da Z-API
def enviar_resposta(chat_id, texto):
    url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"
    payload = {
        "chatId": chat_id,
        "message": texto
    }

    print("🚀 ENVIANDO PARA API:", url)
    print("📦 PAYLOAD:", payload)

    response = requests.post(url, json=payload)
    print("📨 RESPOSTA DA API:", response.status_code, response.text)

# 🔎 Endpoint para teste de status
@app.route("/status", methods=["GET"])
def status():
    return "✅ Bot da Magma X está online!", 200
