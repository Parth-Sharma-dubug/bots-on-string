from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.session import SessionLocal
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyRead, CompanyLogin, LoginResponse
from app.auth.deps import get_current_company_id
router = APIRouter(prefix="/company", tags=["company"])

from app.auth.jwt_handler import create_access_token

SECRET_KEY = "YOUR_SUPER_SECRET_KEY"
ALGORITHM = "HS256"


# ------------------------
# PASSWORD HASHING CONTEXT
# ------------------------
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



# ------------------------
# DB Session
# ------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------
# REGISTER COMPANY
# ------------------------
@router.post("/register", response_model=CompanyRead)
def register_company(payload: CompanyCreate, db: Session = Depends(get_db)):

    # Email check
    if db.query(Company).filter(Company.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Name check
    if db.query(Company).filter(Company.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Company name already exists")

    # Hash password
    hashed_password = hash_password(payload.password)

    company = Company(
        name=payload.name,
        email=payload.email,
        password_hash=hashed_password,
        description=payload.description
    )

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

# ------------------------
# LOGIN COMPANY
# ------------------------
@router.post("/login", response_model=LoginResponse)
def login_company(payload: CompanyLogin, db: Session = Depends(get_db)):

    print("Login request:", payload.email)

    company = db.query(Company).filter(
        Company.email == payload.email
    ).first()

    if not company:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Validate password
    if not verify_password(payload.password, company.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"company_id": company.id})

    print("Login successful for:", company.email)

    return {
        "access_token": token,
        "token_type": "bearer",
        "company": company
    }



# check token validity is already stored in local storage
@router.get("/verify")
def verify(current_company_id: int = Depends(get_current_company_id)):
    return {"message": "ok"}
