from flask import Response
from app.database import DB
from werkzeug.exceptions import BadRequest
from app.utils import ResponseCode


class TodoServ:

    table_name = "todo"

    @classmethod
    def get_all_todos(cls):
        try:
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.table_name}")
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            todos = [dict(zip(column_names, row)) for row in rows]
            cursor.close()
            return ResponseCode.success_response(200, "OK", todos)

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()

    @classmethod
    def get_todo_by_id(cls, id):
        try:
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"""SELECT * FROM {cls.table_name} WHERE id = %s""", (id,))
            row = cursor.fetchone()
            column_name = [desc[0] for desc in cursor.description]

            if row:
                todo = dict(zip(column_name, row))
                cursor.close()
                return ResponseCode.success_response(200, "OK", todo)
            else:
                cursor.close()
                return ResponseCode.not_found_response()

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()

    @classmethod
    def add_todo(cls, data):
        try:
            if not data:
                raise BadRequest("Request payload is missing")
            if "title" not in data or "description" not in data:
                raise BadRequest("Title and description are required")
            title = data["title"]
            description = data["description"]
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                f"""INSERT INTO {cls.table_name} (title, description) VALUES (%s, %s)""",
                (title, description),
            )
            cursor.execute(
                f"""SELECT * FROM {cls.table_name} WHERE title = %s AND description = %s""",
                (title, description),
            )
            row = cursor.fetchone()
            column_name = [desc[0] for desc in cursor.description]
            new_todo = dict(zip(column_name, row))
            conn.commit()
            cursor.close()
            return ResponseCode.success_response(
                201, "Todo created successfully", new_todo
            )

        except BadRequest as e:
            return ResponseCode.bad_request_response(e)

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()

    @classmethod
    def update_todo(cls, id, data):
        try:
            if not data:
                raise BadRequest("Request payload is missing")
            if (
                "title" not in data
                or "description" not in data
                or "is_completed" not in data
            ):
                raise BadRequest("Title, description, and is_completed are required")
            title = data["title"]
            description = data["description"]
            is_completed = data["is_completed"]
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE todo SET title = %s, description = %s, is_completed = %s WHERE id = %s",
                (title, description, is_completed, id),
            )
            cursor.execute(f"""SELECT * FROM {cls.table_name} WHERE id = %s""", (id,))
            row = cursor.fetchone()
            column_name = [desc[0] for desc in cursor.description]
            if row:
                updated_todo = dict(zip(column_name, row))
                conn.commit()
                cursor.close()
                return ResponseCode.success_response(
                    200, "Todo updated successfully", updated_todo
                )
            else:
                cursor.close()
                return ResponseCode.not_found_response()

        except BadRequest as e:
            return ResponseCode.bad_request_response()

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()

    @classmethod
    def delete_todo(cls, id):
        try:
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"""DELETE FROM {cls.table_name} WHERE id = %s""", (id,))
            conn.commit()
            if cursor.rowcount > 0:
                cursor.close()
                return ResponseCode.success_response(200, "Todo deleted successfully")
            else:
                cursor.close()
                return ResponseCode.not_found_response()

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()
