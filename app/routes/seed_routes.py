from flask import Blueprint
from app.services import SeedServ

seeder_bp = Blueprint("seeder", __name__)


@seeder_bp.route("/seeder/todos", methods=["POST"])
def seeder_todos_route():
    return SeedServ.seeder_todos()


@seeder_bp.route("/seeder/todos", methods=["DELETE"])
def delete_todos_route():
    return SeedServ.delete_seeded_todos()
