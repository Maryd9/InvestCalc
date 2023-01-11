from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, APIRouter, Request
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette.responses import HTMLResponse, JSONResponse
from . import forms, config, models, hashing, token
from sqlalchemy.orm import Session
from app.config import get_db
from app.handlers import templates
from .models import User

router = APIRouter(tags=['Authentication'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = token.SECRET_KEY
ALGORITHM = token.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = token.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = forms.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(config.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


@router.post('/login', response_model=forms.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(config.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not hashing.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user: forms.UserCreate, db: Session = Depends(get_db)):
    exists_user = db.query(User.id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already taken',
        )
    # hash the password - user.password
    hashed_password = hashing.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return JSONResponse(content={"message": "User registered"}, status_code=200)
