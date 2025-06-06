from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuração Z-API
ID_INSTANCIA = '3E23640FFCAEC0DC14473274D0A2B459'
TOKEN = '56100423CA70A6B6503E638D'
URL_BASE = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}'

# Enviar texto simples
def enviar_texto(chat_id, texto):
    payload = {"chatId": chat_id, "message": texto}
    try:
        r = requests.post(f"{URL_BASE}/send-text", json=payload)
        print("🔵 ENVIO TEXTO:", r.status_code, r.text)
    except Exception as e:
        print("❌ Erro ao enviar texto:", e)

# Enviar mensagem com opções (texto simples)
def enviar_opcoes(chat_id):
    mensagem_opcoes = (
        "Digite o número para escolher:\n"
        "1️⃣ Renovar\n"
        "2️⃣ Cotar novo\n"
        "3️⃣ Assistência 24h"
    )
    enviar_texto(chat_id, mensagem_opcoes)

# Interpretar mensagem
def interpretar(msg):
    msg = str(msg).strip().lower()
    respostas = {
        "1": "🟢 Vamos renovar seu seguro! Me passe seu CPF ou placa.",
        "2": "📋 Vamos cotar um novo seguro! Qual tipo? (auto, residencial, empresarial...)",
        "3": "🛠️ Assistência 24h acionada! Informe o endereço ou localização."
    }
    return respostas.get(msg, None)

# Extrair mensagem e telefone
def extrair_dados(data):
    msg = data.get("text", {}).get("mensagem") or data.get("text", {}).get("body") or data.get("text") or data.get("mensagem") or data.get("message")
    telefone = data.get("phone") or data.get("telefone") or data.get("sender", {}).get("phone") or data.get("chatId")
    if telefone:
        telefone = str(telefone).replace("-grupo", "").replace("@c.us", "").strip()
    return msg, telefone

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("\n📥 JSON recebido:", data)

    if data.get("isGroup") or "-grupo" in str(data.get("telefone", "")):
        print("🚫 Grupo detectado, ignorado.")
        return jsonify({"status": "ignorado grupo"}), 200

    msg, telefone = extrair_dados(data)
    chat_id = telefone + "@c.us" if telefone else ""
    print(f"💬 Mensagem recebida: '{msg}'")
    print(f"📱 chat_id: {chat_id}")

    if len(telefone) < 12:
        print("⚠️ Telefone curto ou inválido. Não enviado.")
        return jsonify({"status": "telefone curto/ok"}), 200

    resposta = interpretar(msg)
    if resposta:
        enviar_texto(chat_id, resposta)
    else:
        enviar_opcoes(chat_id)

    return jsonify({"status": "ok"}), 200

@app.route("/status", methods=["GET"])
def status():
    return "MAGMA BOT RODANDO", 200
