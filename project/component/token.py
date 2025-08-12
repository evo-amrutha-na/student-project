from project.config.config import *
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import HTTPBearer
import jwt
token_auth_scheme = HTTPBearer()
from project.model.models import *


# admin create token
def admin_create_access_token(student_id: int, day: int = 100) -> str:
    current_datetime = datetime.now(timezone.utc)
    expire_in = current_datetime + timedelta(days=day)
    payload = {
        "id": student_id,
        "created": current_datetime.isoformat(),
        "exp": int(expire_in.timestamp()),  # store as UNIX timestamp
        "token_type": "access_token",
    }
    encoded_jwt = jwt.encode(payload, ACCESS_TOKEN_ADMIN, algorithm="HS256")
    return encoded_jwt

def validate_student_access_token(
    token: str = Depends(token_auth_scheme)):

    try:
        student_id = None

        raw_token = token.credentials

        json_data = jwt.decode(raw_token, ACCESS_TOKEN_ADMIN, algorithms=["HS256"])

        user_id = json_data.get("id")
        exp_ts = json_data.get("exp")
        token_type = json_data.get("token_type")

        if token_type != "access_token":
            logger.info("Invalid token type")
            return None

        if not user_id or not exp_ts:
            logger.info("Token missing id or exp")
            return None

        try:
            expiry = datetime.fromtimestamp(int(exp_ts), tz=timezone.utc)
        except Exception:
            logger.info("Invalid exp value in token")
            return None

        db_student = session.query(Student).filter(Student.id == user_id).first()
        if not db_student:
            logger.info("User is not found")
            return None

        if not db_student.active:
            logger.info("User is blocked")
            return None

        logger.info(f"Active User :: {db_student.fname} {db_student.lname} :: {db_student.email}")

        if datetime.now(timezone.utc) < expiry:
            student_id = user_id
        else:
            logger.info("Token Expired")
            student_id = None

        return student_id

    except jwt.ExpiredSignatureError:
        logger.info("JWT expired")
        return None
    except jwt.DecodeError:
        logger.info("JWT decode error")
        return None
    except Exception as e:
        logger.info(f"[ERROR] : {str(e)}")
        return None