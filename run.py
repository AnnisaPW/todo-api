# run.py
import os

from flask import jsonify
from app import create_app
from flask_jwt_extended import JWTManager

app = create_app("development")

# PORT = os.environ.get("PORT", 5151)
jwt = JWTManager(app)


@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({"error": "missing or invalid token"}), 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5151, debug=True)
