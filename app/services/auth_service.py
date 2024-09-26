import email
from flask import Response, jsonify, request
from app.utils import Validator, Generator
from app.database import DB


class AuthServ:

    @staticmethod
    def register_user(request):
        user_email = request["email"]
        user_pass = request["password"]
        user_pass_confirm = request["confirm_password"]

        # Check if the email already exists in the database
        existing_user = DB.read_db(
            """SELECT * FROM users WHERE email = %s""", (user_email,)
        )
        if existing_user:
            # Email already exists, return 409 Conflict
            return Response("Email already exists", status=409)

        if user_pass == user_pass_confirm and Validator.validate_user_input(
            "authentication", email=user_email, password=user_pass
        ):
            salt_pass = Generator.generate_salt()
            hash_pass = Generator.generate_hash(user_pass, salt_pass)

            # Debugging prints
            print(f"Registering User - Salt: {salt_pass}")
            print(f"Registering User - Hashed Password: {hash_pass}")

            if DB.write_db(
                """INSERT INTO users (email, password_salt, password_hash) VALUES (%s, %s, %s)""",
                (
                    user_email,
                    salt_pass,
                    hash_pass,
                ),
            ):
                return Response(status=201)
            else:
                return Response(
                    status=500
                )  # Use 500 if something goes wrong on the server
        else:
            return Response(status=400)  # Bad request for invalid input

    @staticmethod
    def login_user(request):
        user_email = request["email"]
        user_password = request["password"]

        # Validate user and retrieve token or error message
        validation_result = Validator.validate_user(user_email, user_password)

        if isinstance(
            validation_result, str
        ):  # If validation returned an error message
            return jsonify({"error": validation_result}), 401
        elif validation_result:  # Valid token returned
            return jsonify({"jwt_token": validation_result})
        else:
            return jsonify({"error": "Login failed due to an unknown error"}), 401
