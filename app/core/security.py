"""
Enterprise JWT Security
"""

from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = "CHANGE_THIS_TO_ENV_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


security = HTTPBearer()


# =========================
# CREATE TOKEN
# =========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(

        minutes=ACCESS_TOKEN_EXPIRE_MINUTES

    )

    to_encode.update(

        {"exp": expire}

    )

    encoded_jwt = jwt.encode(

        to_encode,

        SECRET_KEY,

        algorithm=ALGORITHM

    )

    return encoded_jwt


# =========================
# VERIFY TOKEN
# =========================

def verify_token(

    credentials: HTTPAuthorizationCredentials = Security(security)

):

    token = credentials.credentials

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )

        return payload

    except JWTError:

        raise HTTPException(

            status_code=401,

            detail="Invalid or expired token"

        )
