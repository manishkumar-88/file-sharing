import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta,timezone
from configs import settings  
from utils.exception import CustomException
  
def generate_verification_token(email):
    """Generates a JWT token for email verification."""
    payload = {
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24), 
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")
    return token



def verify_token(token: str) -> dict:
    """
    Verifies a JWT token and returns the decoded data.
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms='HS256')
        return payload
    
    except ExpiredSignatureError:
        raise ValueError("The token has expired.")
    except Exception as ex:
        raise CustomException(ex)
