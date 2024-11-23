from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.model import DonationHistory
from sqlmodel import Session, select, func
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.database.model import Admins
from app.core import app, get_session
from app.model.admin import Admin
from pydantic import BaseModel
from jose import JWTError, jwt

SECRET_KEY = "0fc6d75a9ae8bc21eb01ee28bd14ed71e1549eadc91080900f8274ac2fcb6955"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer("token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(session: Session, username: str):
    statement = select(Admins).where(Admins.username == username)
    return session.exec(statement).first()


def authenticate_user(session: Session, username: str, password: str):
    user = get_user(session, username)
    if not user or not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credential_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user(session=session, username=token_data.username)
    if not user:
        raise credential_exception
    return user


async def get_current_active_user(current_user: Admins = Depends(get_current_user)):
    return current_user


def get_donation_counts(session: Session):
    date_conversion = func.date(
        func.concat(
            func.substr(DonationHistory.date, 7, 4),
            '-',
            func.substr(DonationHistory.date, 4, 2),
            '-',
            func.substr(DonationHistory.date, 1, 2),
        )
    )

    def format_results(results, labels):
        return [dict(zip(labels, row)) for row in results]

    daily_results = session.query(
        date_conversion.label("day"),
        func.count(DonationHistory.id).label("donation_count")
    ).group_by(date_conversion).all()
    daily = format_results(daily_results, ["daily", "donation_count"])

    return {"daily": daily}


@app.post("/token", response_model=Token, tags=["Admin"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/admin/me/", tags=["Admin"])
async def read_users_me(current_user: Admins = Depends(get_current_active_user)):
    return current_user

@app.post('/api/admin', tags=['Admin'])
async def create_admin(admin: Admin, session: Session = Depends(get_session)):
    statement = select(Admins).where(Admins.username == admin.username)
    result = session.exec(statement).first()
    if result:
        raise HTTPException(status_code=406, detail="This admin already exists")

    new_admin = Admins(
        name=admin.name,
        username=admin.username,
        password=get_password_hash(admin.password)
    )
    session.add(new_admin)
    session.commit()
    session.refresh(new_admin)
    return {'message': 'Admin successfully created', 'admin': new_admin}
