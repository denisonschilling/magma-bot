from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# === Configurações da Instância Z-API ===
ZAPI_URL = "https://api.z-api.io/instances/3E23640FFCAC0EDC14473274D0A2B459/token/56100423CA70A6B650E3638D/send-text"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Mensagem recebida:", data)

    if data and "messages" in data:
        for msg in data["messages"]:
            numero = msg.get("from")
            texto = msg.get("text", {}).get("body", "")

            if numero and texto:
                print(f"👉 De: {numero} | Texto: {texto}")

                payload = {
                    "phone": numero,
                    "message": f"Olá, recebi sua mensagem: *{texto}* ✅"
                }

                try:
                    resposta = requests.post(ZAPI_URL, json=payload)
                    print("✅ Enviado:", resposta.status_code, resposta.text)
                except Exception as e:
                    print("❌ Erro ao enviar:", e)

    return jsonify({"message": "OK"}), 200
