from flask import jsonify
from app.database import get_db_connection
from app.models import seed_todos
from app.utils import success_response, server_error_response, not_found_response, bad_request_response


tableName = 'todo'


def seeder_todos():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    for todo in seed_todos:
      cursor.execute(
        f'''INSERT INTO {tableName} (title, description) VALUES (%s, %s)''',(todo['title'], todo['description'])
      )
    conn.commit()
    cursor.close()
    return success_response(201, "Todos seeded successfully")

  except Exception as e:
    print(f"Error: {e}")
    return server_error_response()

def delete_seeded_todos():
  try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {tableName}')
    conn.commit()
    cursor.close()
    return success_response(200,'Seeded todos deleted successfully')

  except Exception as e:
    print(f"Error: {e}")
    return server_error_response()