from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot da Magma X está online com Render!"

@app.route("/agendar", methods=["POST"])
def agendar():
    data = request.get_json()

    # Exemplo de dados esperados no corpo da requisição
    titulo = data.get("titulo")
    data_evento = data.get("data")  # Ex: "2025-06-12"
    hora_evento = data.get("hora")  # Ex: "09:00"

    # Aqui futuramente chamaremos a integração com Google Agenda
    return jsonify({
        "mensagem": "Lembrete recebido!",
        "titulo": titulo,
        "data": data_evento,
        "hora": hora_evento
    }), 200
