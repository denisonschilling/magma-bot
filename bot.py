from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ZAPI_URL = "https://api.z-api.io/instances/3E23640FFCAC0EDC14473274D0A2B459/token/56100423CA70A6B650E3638D/send-text"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📥 Dados recebidos:", data)

    if not data or "messages" not in data:
        return jsonify({"status": "Ignorado"}), 200

    for msg in data["messages"]:
        numero = msg.get("from")

        # Tenta capturar a mensagem de dois formatos possíveis
        texto = ""
        if msg.get("text", {}).get("body"):
            texto = msg["text"]["body"]
        elif msg.get("text", {}).get("mensagem"):
            texto = msg["text"]["mensagem"]

        if numero and texto:
            print(f"✉️ Número: {numero} | Texto: {texto}")

            payload = {
                "phone": numero,
                "message": f"Olá! Recebi sua mensagem: *{texto}* ✅"
            }

            try:
                resposta = requests.post(ZAPI_URL, json=payload)
                print("✅ Enviado:", resposta.status_code, resposta.text)
            except Exception as e:
                print("❌ Erro ao enviar resposta:", e)

    return jsonify({"status": "Processado"}), 200
