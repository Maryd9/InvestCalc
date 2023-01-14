from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter(tags=['Default'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/home', response_class=HTMLResponse, name='Show Main Form')
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/signin', response_class=HTMLResponse, name='Show Login Form')
async def home(request: Request):
    return templates.TemplateResponse('signin.html', {'request': request})

#
# @router.get('/user', name='user:get')
# def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
#     user = database.query(User).filter(User.id == token.user_id).one_or_none()
#     return {'user': user.get_filtered_data()}
