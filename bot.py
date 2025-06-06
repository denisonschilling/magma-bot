from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ZAPI_URL = "https://api.z-api.io/instances/3E23640FFCAC0EDC14473274D0A2B459/token/56100423CA70A6B650E3638D/send-text"
CLIENT_TOKEN = "F9edb1f0692041b9abc68ec7f6226575"  # atualiza se mudar

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Dados recebidos:", data)

    if not data or "messages" not in data:
        return jsonify({"status": "Ignorado"}), 200

    for msg in data["messages"]:
        numero = msg.get("from")

        # Captura robusta do texto
        texto_raw = msg.get("text", {})
        texto = texto_raw.get("body") or texto_raw.get("mensagem") or ""

        if numero and texto:
            print(f"✉️ Número: {numero} | Texto: {texto}")

            payload = {
                "phone": numero,
                "message": f"👋 Olá! Você enviou: *{texto}*"
            }

            headers = {
                "Content-Type": "application/json",
                "client-token": CLIENT_TOKEN
            }

            try:
                resposta = requests.post(ZAPI_URL, json=payload, headers=headers)
                print("✅ Enviado:", resposta.status_code, resposta.text)
            except Exception as e:
                print("❌ Erro ao enviar resposta:", e)

    return jsonify({"status": "OK"}), 200
