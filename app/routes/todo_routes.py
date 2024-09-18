# app/routes/todo_routes.py
from flask import Blueprint, jsonify, request
from app.services import TodoServ

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/todos", methods=["GET"])
def read_todos():
    return TodoServ.get_all_todos()


@todo_bp.route("/todos/<string:id>", methods=["GET"])
def read_todo_by_id(id):
    return TodoServ.get_todo_by_id(id)


@todo_bp.route("/todos", methods=["POST"])
def create_todo():
    return TodoServ.add_todo(request.json)


@todo_bp.route("/todos/<string:id>", methods=["PUT"])
def update_todo_item(id):
    return TodoServ.update_todo(id, request.json)


@todo_bp.route("/todos/<string:id>", methods=["DELETE"])
def delete_todo_item(id):
    return TodoServ.delete_todo(id)
