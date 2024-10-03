from datetime import timedelta
from flask import Response, jsonify
from flask_jwt_extended import create_access_token
from app.utils import Validator, Generator
from app.database import DB
from app.config import Config


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
        user_token = Validator.validate_user(user_email, user_password)

        if not user_token:
            return jsonify({"error": "Incorrect email or password"}), 401
        else:
            # Create a JWT token with an expiration time
            access_token = create_access_token(
                identity=user_email,
                expires_delta=timedelta(seconds=int(Config.JWT_ACCESS_TOKEN_EXPIRES)),
            )
            return jsonify({"jwt_token": access_token})
