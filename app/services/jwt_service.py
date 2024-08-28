from time import timezone
import jwt
import datetime
from flask import current_app

class JWTService:

  @staticmethod
  def encode_token(user_id):
    """
    Generate the Auth Token
    :param user_id: int
    :return: string
    """
    try:
      payload = {
        'exp': datetime.now(timezone.utc) + datetime.timedelta(days=1),
        'iat': datetime.now(timezone.utc),
        'sub': user_id
      }
      return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm="HS256"
      )
    except Exception as e:
      return str(e)
    
  @staticmethod
  def decode_token(token):
    """
    Decodes the Auth Token
    :param token: string
    :return: integer|string
    """
    try:
      payload = jwt.decode(token, current_app.config.get('SECRET_KEY'), algorithms=["HS256"],)
      return payload['sub']
    except jwt.ExpiredSignatureError as e:
      print(str(e))
      return 'Token expired. Please log in again'
    except jwt.InvalidTokenError as e:
      print(str(e))
      return 'Invalid token. Please log in again'