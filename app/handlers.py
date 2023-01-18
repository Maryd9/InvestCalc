from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter(tags=['Get form'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/home', response_class=HTMLResponse, name='Main page')
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/signin', response_class=HTMLResponse, name='Login form')
def home(request: Request):
    return templates.TemplateResponse('signin.html', {'request': request})


@router.get("/home/user/{id}", response_class=HTMLResponse, name='Main page after login')
def users(request: Request):
    return templates.TemplateResponse('homeUser.html', {'request': request})


@router.get('/savedresults/user/{id}', response_class=HTMLResponse, name='All saved result of user')
def home(request: Request):
    return templates.TemplateResponse('savedResults.html', {'request': request})

#
# @router.get('/user', name='user:get')
# def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
#     user = database.query(User).filter(User.id == token.user_id).one_or_none()
#     return {'user': user.get_filtered_data()}
