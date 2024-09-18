from flask import jsonify
from app.database import DB
from app.models import Todo
from app.utils import ResponseCode


seed_todos = [
    Todo(title="Finish homework", description="Complete math and science assignments"),
    Todo(title="Call mom", description="Jog around the park for 30 minutes"),
    Todo(title="Buy groceries", description="Get fruits, vegetables, and snacks"),
    Todo(title="Watch a movie", description="Watch the latest episode of Sherlock"),
    Todo(title="Read a book", description='Finish reading "To Kill a Mockingbird"'),
    Todo(title="Clean the house", description="Vacuum and dust all rooms"),
    Todo(title="Prepare dinner", description="Cook pasta with garlic bread"),
    Todo(title="Work on project", description="Complete Flask API development"),
    Todo(title="Meditate", description="Spend 15 minutes on mindfulness meditation"),
    # {
    #     "title": "Finish homework",
    #     "description": "Complete math and science assignments",
    # },
    # {"title": "Go for a run", "description": "Jog around the park for 30 minutes"},
    # {"title": "Call mom", "description": "Catch up with mom over the phone"},
    # {"title": "Buy groceries", "description": "Get fruits, vegetables, and snacks"},
    # {"title": "Watch a movie", "description": "Watch the latest episode of Sherlock"},
    # {"title": "Read a book", "description": 'Finish reading "To Kill a Mockingbird"'},
    # {"title": "Clean the house", "description": "Vacuum and dust all rooms"},
    # {"title": "Prepare dinner", "description": "Cook pasta with garlic bread"},
    # {"title": "Work on project", "description": "Complete Flask API development"},
    # {"title": "Meditate", "description": "Spend 15 minutes on mindfulness meditation"},
]


def generate_seeder() -> list:
    todo_list: list = []

    for todo in seed_todos:
        todo_dic = Todo.to_dict(todo)
        todo_list.append(todo_dic)

    return todo_list


class SeedServ:
    tableName = "todo"

    @classmethod
    def seeder_todos(cls):
        try:
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            for todo in generate_seeder():
                cursor.execute(
                    f"""INSERT INTO {cls.tableName} (title, description) VALUES (%s, %s)""",
                    (todo["title"], todo["description"]),
                )
            conn.commit()
            cursor.close()
            return ResponseCode.success_response(201, "Todos seeded successfully")

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()

    @classmethod
    def delete_seeded_todos(cls):
        try:
            conn = DB.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {cls.tableName}")
            conn.commit()
            cursor.close()
            return ResponseCode.success_response(
                200, "Seeded todos deleted successfully"
            )

        except Exception as e:
            print(f"Error: {e}")
            return ResponseCode.server_error_response()
