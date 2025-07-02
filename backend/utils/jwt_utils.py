import jwt
import datetime

SECRET_KEY = "your-very-secure-secret"  # Replace with env var in production
ALGORITHM = "HS256"
EXPIRY_HOURS = 1

def generate_token(user_email, role):
    payload = {
        "user": user_email,
        "role": role,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=EXPIRY_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
