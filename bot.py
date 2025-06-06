from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# === CONFIGURAÇÕES Z-API ===
ID_INSTANCIA = "3E23640FFCAC0EDC14473274D0A2B459"
TOKEN = "56100423CA70A6B650E3638D"
URL_ENVIO = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-text"

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("🔔 Webhook recebido:", json.dumps(data, indent=2))

        if data and 'messages' in data:
            for msg in data['messages']:
                texto = msg.get('text', {}).get('body', '')
                numero = msg.get('from')

                if texto and numero:
                    print(f"📨 Mensagem: {texto} | De: {numero}")

                    payload = {
                        "phone": numero,
                        "message": f"👋 Oi! Recebi sua mensagem: *{texto}*"
                    }

                    headers = {
                        "Content-Type": "application/json"
                    }

                    print(f"🚀 Enviando para Z-API: {json.dumps(payload)}")

                    resposta = requests.post(URL_ENVIO, json=payload, headers=headers)
                    print(f"✅ STATUS: {resposta.status_code}")
                    print(f"📦 RESPOSTA: {resposta.text}")

        return jsonify({"message": "OK"}), 200

    except Exception as e:
        print("❌ ERRO GERAL:", str(e))
        return jsonify({"error": "Erro no webhook"}), 500
