from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.auth.jwt_handler import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/company/login")

def get_current_company_id(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)

    if payload is None or "company_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload["company_id"]
