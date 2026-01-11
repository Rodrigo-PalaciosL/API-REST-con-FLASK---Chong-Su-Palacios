from flask import Flask, jsonify, request
from db import get, post, put, delete

app = Flask(__name__)

@app.route("/")
def main():
    return jsonify({"mensaje": "API REST con Flask"}), 200


# GET – obtener todos los usuarios
@app.route("/users", methods=["GET"])
def get_users():
    users = get()
    return jsonify(users), 200


# POST – crear usuario
@app.route("/users", methods=["POST"])
def create_user():
    if not request.json:
        return jsonify({"error": "No se enviaron datos"}), 400

    if "name" not in request.json or "email" not in request.json:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    success, error = post(request.json)

    if not success and error == "EMAIL_DUPLICADO":
        return jsonify({"error": "El email ya existe"}), 409

    return jsonify({"mensaje": "Usuario creado correctamente"}), 201


# PUT – actualizar usuario
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    if not request.json:
        return jsonify({"error": "No se enviaron datos"}), 400

    success = put(id, request.json)

    if not success:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario actualizado"}), 200


# DELETE – eliminar usuario
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    success = delete(id)

    if not success:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": "Usuario eliminado"}), 200


# Manejo de rutas inexistentes
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Ruta no encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)
