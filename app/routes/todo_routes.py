# app/routes/todo_routes.py
from flask import Blueprint, jsonify, redirect, request
from flask_jwt_extended import jwt_required
from app.services import TodoServ

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/", methods=["GET"], endpoint="init_route")
def init_route():
    return redirect("/todos")


@todo_bp.route("/todos", methods=["GET"])
def read_todos():
    return TodoServ.get_all_todos()


@todo_bp.route("/todos/<string:id>", methods=["GET"], endpoint="read_all_todos")
def read_todo_by_id(id):
    return TodoServ.get_todo_by_id(id)


@todo_bp.route("/todos", methods=["POST"], endpoint="create_todo")
@jwt_required()
def create_todo():
    return TodoServ.add_todo(request.json)


@todo_bp.route("/todos/<string:id>", methods=["PUT"], endpoint="update_todo_item")
@jwt_required()
def update_todo_item(id):
    return TodoServ.update_todo(id, request.json)


@todo_bp.route("/todos/<string:id>", methods=["DELETE"], endpoint="delete_todo_item")
@jwt_required()
def delete_todo_item(id):
    return TodoServ.delete_todo(id)
