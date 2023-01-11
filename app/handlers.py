from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates
from starlette.responses import HTMLResponse


router = APIRouter(tags=['Default'])
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse, name='Show Main Form')
def home(request: Request):
    return templates.TemplateResponse('html/home.html',
                                      {'request': request})


@router.get('/login', response_class=HTMLResponse, name='Show Login Form')
async def home(request: Request):
    return templates.TemplateResponse('html/login.html', {'request': request})




# @router.post('/login', name='user:login')
# def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
#     user = database.query(User).filter(User.email == user_form.email).one_or_none()
#     if not user or get_password_hash(user_form.password) != user.password:
#         return {'error': 'Email/password doesnt match'}
#
#     auth_model = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
#     database.add(auth_model)
#     database.commit()
#     return {'auth_token': auth_model.token}

#
# @router.get('/user', name='user:get')
# def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
#     user = database.query(User).filter(User.id == token.user_id).one_or_none()
#     return {'user': user.get_filtered_data()}
#
#
# @router.post('/user', name='user:create')
# def create_user(user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)):
#     exists_user = database.query(User.id).filter(User.email == user.email).one_or_none()
#     if exists_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Email already taken',
#         )
#
#     new_user = User(
#         email=user.email,
#         password=get_password_hash(user.password),
#         login=login
#     )
#     database.add(new_user)
#     database.commit()
#     return {'user_id': new_user.id}
#
