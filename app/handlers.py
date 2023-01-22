from fastapi import APIRouter, Request, Depends, Form, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app import models
from app.config import get_db

router = APIRouter(tags=['Get form'])
templates = Jinja2Templates(directory='app/templates')
security = HTTPBearer()


# redirection block
class RequiresLoginException(Exception):
    pass


def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
    return self.decode_token(auth.credentials)


@router.get('/', response_class=HTMLResponse, name='Main page')
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/signin', response_class=HTMLResponse, name='Login form')
def home(request: Request):
    return templates.TemplateResponse('signin.html', {'request': request})


# @router.post("/user", response_class=RedirectResponse, name='Main page after login')
# def users(userid: str = Form(...), db: Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == userid).first()
#     return RedirectResponse(f"/home/user/{userid}", status_code=200)


@router.get("/user/", response_class=HTMLResponse, name='Main page after login')
def users(request: Request, db: Session = Depends(get_db)):
    # user = db.query(models.Users).filter(models.Users.id == userid).first()
    return templates.TemplateResponse('homeUser.html', {'request': request})


@router.get('/savedresults/user', response_class=HTMLResponse, name='All saved result of user')
def home(request: Request, db: Session = Depends(get_db)):
    password = request.cookies.get('Authorization')
    user = db.query(models.Users).filter(models.Users.password == password).one_or_none()
    print(user)
    try:
        return templates.TemplateResponse('savedResults.html', {'request': request})
    except:
        raise RequiresLoginException()


@router.get('/logout', response_class=HTMLResponse, name='Logout')
def home(request: Request):
    request.session.clear()
    return templates.TemplateResponse('index.html', {'request': request})

# #
# # @router.get('/user', name='user:get')
# # def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
# #     user = database.query(User).filter(User.id == token.user_id).one_or_none()
# #     return {'user': user.get_filtered_data()}

