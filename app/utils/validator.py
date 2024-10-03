from app.database import DB
from app.utils import Generator


class Validator:

    @staticmethod
    def validate_user_input(input_type, **kwargs):
        if input_type == "authentication":
            if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
                return True
            else:
                return False

    @staticmethod
    def validate_user(email, password):
        current_user = DB.read_db("""SELECT * FROM users WHERE email = %s""", (email,))

        if len(current_user) != 1:
            return "User does not exist"

        saved_password_hash = current_user[0][3]
        saved_password_salt = current_user[0][2]

        # Print saved salt and password hash for comparison
        print(f"Login User - Saved Salt: {saved_password_salt}")
        print(f"Login User - Saved Hashed Password: {saved_password_hash}")

        # Calculate the hash of the provided password
        calculated_password_hash = Generator.generate_hash(
            password, saved_password_salt
        )

        # Print calculated hash for debugging
        print(f"Login User - Calculated Hashed Password: {calculated_password_hash}")

        if calculated_password_hash != saved_password_hash:
            return "Incorrect password"

        user_id = current_user[0][0]
        jwt_token = Generator.generate_jwt_token({"id": user_id})

        return jwt_token
