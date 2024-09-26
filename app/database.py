# app/database.py
from pydoc import classname
from flask_mysqldb import MySQL

mysql = MySQL()


class DB:

    @staticmethod
    def get_db_connection():
        """Utility function to get a database connection."""
        return mysql.connection

    @staticmethod
    def init_db(app):
        """Initialize the database and create tables if they don't exist."""
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute(
                """CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_salt VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);"""
            )
            cursor.execute(
                """
              CREATE TABLE IF NOT EXISTS todo (
                  id INT AUTO_INCREMENT PRIMARY KEY,
                  title VARCHAR(255) NOT NULL,
                  description TEXT,
                  is_completed BOOLEAN NOT NULL DEFAULT 0
              )
          """
            )
            cursor.execute(
                """
            ALTER TABLE todo
            ADD COLUMN created_at INT NOT NULL DEFAULT (UNIX_TIMESTAMP())
          """
            )
            cursor.execute(
                """
            ALTER TABLE todo
            ADD COLUMN updated_at INT DEFAULT NULL;

          """
            )
            cursor.execute(
                """
            DELIMITER $$
              CREATE TRIGGER update_updated_at
                BEFORE UPDATE ON todo
                FOR EACH ROW
                BEGIN
                    SET NEW.updated_at = UNIX_TIMESTAMP();
                END$$

            DELIMITER;
          """
            )
            mysql.connection.commit()
            cursor.close()

    @staticmethod
    def write_db(query, params):
        cursor = mysql.connection.cursor()

        try:
            cursor.execute(query, params)
            mysql.connection.commit()
            cursor.close()
            return True

        except Exception as e:
            cursor.close()
            return False

    @staticmethod
    def read_db(query, params=None):
        cursor = mysql.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        entries = cursor.fetchall()
        cursor.close()

        content = []

        for entry in entries:
            content.append(entry)

        return content
