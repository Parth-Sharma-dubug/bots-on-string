from fastapi import Depends, HTTPException
from jose import jwt, JWTError

def get_current_company(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        company_id = payload.get("company_id")
        return company_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
