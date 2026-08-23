from flask import Flask, request, jsonify

app = Flask(__name__)

users = [
    {"id": 1, "name": "Ana Souza", "email": "ana@email.com"},
    {"id": 2, "name": "Bruno Lima", "email": "bruno@email.com"}
]

next_id = 3

@app.route("/")
def home():
    return jsonify({"message": "API funcionando"}), 200

@app.route("/users", methods=["GET"])
def list_users():
    return jsonify({"data": users}), 200

@app.route("/users", methods=["POST"])
def create_user():
    global next_id
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Campos obrigatórios: name e email"}), 400

    new_user = {
        "id": next_id,
        "name": data["name"],
        "email": data["email"]
    }

    users.append(new_user)
    next_id += 1

    return jsonify({"data": new_user}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({"data": user}), 200

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Campos obrigatórios: name e email"}), 400

    user["name"] = data["name"]
    user["email"] = data["email"]

    return jsonify({"data": user}), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)

    if user is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    users.remove(user)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)