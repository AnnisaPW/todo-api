from flask import Blueprint
from app.services import seeder_todos, delete_seeded_todos

seeder_bp = Blueprint('seeder', __name__)

@seeder_bp.route('/seeder/todos', methods=['POST'])
def seeder_todos_route():
  return seeder_todos()

@seeder_bp.route('/seeder/todos', methods=['DELETE'])
def delete_todos_route():
  return delete_seeded_todos()
