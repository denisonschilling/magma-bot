from flask import Flask, request, jsonify

app = Flask(__name__)

# Token de segurança da conta
EXPECTED_TOKEN = "F9eddb1f0692041b9abc8e8ec7f622657S"

@app.route("/", methods=["POST"])
def webhook():
    token = request.headers.get("client-token")
    if token != EXPECTED_TOKEN:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    # Extrair mensagem e número de telefone
    message = data.get("message", {}).get("text", "")
    phone = data.get("message", {}).get("phone", "")

    print(f"Mensagem recebida de {phone}: {message}")

    # Se a mensagem for "oi", responde automaticamente
    if "oi" in message.lower():
        return jsonify({
            "phone": phone,
            "message": "Olá! Aqui é o Magma Bot. Como posso te ajudar hoje?"
        })

    # Sempre retornar 'RECEIVED' para evitar reenvio da Z-API
    return jsonify({"status": "RECEIVED"})
