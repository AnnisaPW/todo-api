from flask import Blueprint, request
from app.services import AuthServ

auth_bp = Blueprint("authentication", __name__)


@auth_bp.route("/register", methods=["POST"])
def register_user():
    return AuthServ.register_user(request=request.json)


@auth_bp.route("/login", methods=["POST"])
def login_user():
    return AuthServ.login_user(request=request.json)
