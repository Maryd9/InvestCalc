from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, APIRouter, Request
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette.responses import JSONResponse, HTMLResponse
from . import forms, config, models, hashing, token
from sqlalchemy.orm import Session
from app.config import get_db, SQLALCHAMY_DATABASE_URL
from .forms import UserLogin
from .handlers import templates, users, RequiresLoginException
from .models import Users
from databases import Database

router = APIRouter(tags=['Authentication'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")

SECRET_KEY = token.SECRET_KEY
ALGORITHM = token.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = token.ACCESS_TOKEN_EXPIRE_MINUTES

database = Database(SQLALCHAMY_DATABASE_URL)


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


async def authenticate_user(self, username, password):
    try:
        user = UserLogin(email=username, password=password)
        query = users.select().where(users.c.email == user.email)
        result = await database.fetch_one(query)
        if result:
            password_check = self.verify_password(user.password, result[2])
            return password_check
        else:
            return False
    except:
        raise RequiresLoginException()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(config.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user


@router.post('/signin', response_model=forms.Token)
async def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(config.get_db)):
    try:
        user = db.query(models.Users).filter(
            models.Users.email == user_credentials.username).first()
        if await authenticate_user(user.email, user.password):
            atoken = create_access_token(user.email)
            response = templates.TemplateResponse("success.html",
                                                  {"request": request, "USERNAME": user.email,
                                                   "success_msg": "Welcome back! ",
                                                   "path_route": '/private/', "path_msg": "Go to your private page!"})

            response.set_cookie(key="Authorization", value=f"{atoken}", httponly=True)
            return response
        if not user:
            return templates.TemplateResponse("error.html",
                                              {"request": request, 'detail': 'Incorrect Username or Password',
                                               'status_code': 403})
        if not hashing.verify(user_credentials.password, user.password):
            return templates.TemplateResponse("error.html",
                                              {"request": request, 'detail': 'Incorrect Username or Password',
                                               'status_code': 403})

    except Exception as err:
        return templates.TemplateResponse("error.html",
                                          {"request": request, 'detail': 'Incorrect Username or Password',
                                           'status_code': 401})

    # if not user:
    #     return JSONResponse(content={"message": "Email already taken"}, status_code=403)
    #     # raise HTTPException(
    #     #     status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    #
    # if not hashing.verify(user_credentials.password, user.password):
    #     return JSONResponse(content={"message": "Email already taken"}, status_code=403)
    #     # raise HTTPException(
    #     #     status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    #
    # access_token = create_access_token(data={"user_id": user.id})
    #
    # return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_class=HTMLResponse)
async def create_user(request: Request, user: forms.UserCreate, db: Session = Depends(get_db)):
    exists_user = db.query(Users.id).filter(Users.email == user.email).one_or_none()
    if exists_user:
        return JSONResponse(content={"message": "Email already taken"}, status_code=200)
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST,
        #     detail='Email already taken',
        # )
    # hash the password - user.password
    hashed_password = hashing.hash(user.password)
    user.password = hashed_password

    new_user = Users(
        role_id=2,
        username=user.username,
        email=user.email,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"user_id": new_user.id})

    # return JSONResponse(content={"message": "OK", "user_id": new_user.id, "access_token": access_token},
    #                     status_code=200)
    response = templates.TemplateResponse("success.html",
                                          {"request": request, "success_msg": "Registration Successful!",
                                           "path_route": '/', "path_msg": "Click here to login!"})
    return response
