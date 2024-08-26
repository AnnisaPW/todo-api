from app.database import get_db_connection
from werkzeug.exceptions import BadRequest
from app.utils import success_response, server_error_response, not_found_response, bad_request_response



table_name = 'todo'

def get_all_todos():
    try:
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(f'SELECT * FROM {table_name}')
      rows = cursor.fetchall()
      column_names = [desc[0] for desc in cursor.description]
      todos = [dict(zip(column_names, row)) for row in rows]
      cursor.close()
      return success_response(200, 'OK', todos)
      
    except Exception as e:
      print(f'Error: {e}')
      return server_error_response()

def get_todo_by_id(id):
    try:
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(f'''SELECT * FROM {table_name} WHERE id = %s''', (id,))
      row = cursor.fetchone()
      column_name = [desc[0] for desc in cursor.description]

      if row:
         todo = dict(zip(column_name, row))
         cursor.close()
         return success_response(200, "OK", todo)
      else:
         cursor.close()
         return not_found_response()
      
    except Exception as e:
      print(f'Error: {e}')
      return server_error_response()

def add_todo(data):
    try:
      if not data:
         raise BadRequest('Request payload is missing')
      if 'title' not in data or 'description' not in data:
         raise BadRequest('Title and description are required')
      title = data['title']
      description = data['description']
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(f'''INSERT INTO {table_name} (title, description) VALUES (%s, %s)''', (title, description))
      cursor.execute(f'''SELECT * FROM {table_name} WHERE title = %s AND description = %s''', (title, description))
      row = cursor.fetchone()
      column_name = [desc[0] for desc in cursor.description]
      new_todo = dict(zip(column_name, row))
      conn.commit()
      cursor.close()
      return success_response(201, "Todo created successfully", new_todo)
      
    except BadRequest as e:
      return bad_request_response(e)
    
    except Exception as e:
       print(f"Error: {e}")
       return server_error_response()

def update_todo(id, data):
    try:
      if not data:
         raise BadRequest('Request payload is missing')
      if 'title' not in data or 'description' not in data or 'is_completed' not in data:
         raise BadRequest('Title, description, and is_completed are required')
      title = data['title']
      description = data['description']
      is_completed = data['is_completed']
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute('UPDATE todo SET title = %s, description = %s, is_completed = %s WHERE id = %s',
                    (title, description, is_completed, id))
      cursor.execute(f'''SELECT * FROM {table_name} WHERE id = %s''', (id,))
      row = cursor.fetchone()
      column_name = [desc[0] for desc in cursor.description]
      if row:
        updated_todo = dict(zip(column_name, row))
        conn.commit()
        cursor.close()
        return success_response(200, "Todo updated successfully", updated_todo)
      else:
         cursor.close()
         return not_found_response()

    except BadRequest as e:
      return bad_request_response()
    
    except Exception as e:
       print(f"Error: {e}")
       return server_error_response()

def delete_todo(id):
    try:
      conn = get_db_connection()
      cursor = conn.cursor()
      cursor.execute(f'''DELETE FROM {table_name} WHERE id = %s''', (id,))
      conn.commit()
      if cursor.rowcount > 0:
          cursor.close()
          return success_response(200, "Todo deleted successfully")
      else:
          cursor.close()
          return not_found_response()
      
    except Exception as e:
      print(f"Error: {e}")
      return server_error_response()
