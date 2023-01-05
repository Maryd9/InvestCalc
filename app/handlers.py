import uuid
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from starlette import status
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.models import connect_db, User, AuthToken, StreamStatus
from app.forms import UserLoginForm, UserCreateForm
from app.auth import check_auth_token
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND
from app.utils import get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('html/home.html',
                                      {'request': request})


@router.get('/login', response_class=HTMLResponse, name='login')
def home(request: Request):
    return templates.TemplateResponse('html/login.html', {'request': request})


@router.post('/login', name='user:login')
def login(user_form: UserLoginForm = Body(..., embed=True), database=Depends(connect_db)):
    user = database.query(User).filter(User.email == user_form.email).one_or_none()
    if not user or get_password_hash(user_form.password) != user.password:
        return {'error': 'Email/password doesnt match'}

    auth_model = AuthToken(token=str(uuid.uuid4()), user_id=user.id)
    database.add(auth_model)
    database.commit()
    return {'auth_token': auth_model.token}


@router.get('/user', name='user:get')
def get_user(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
    user = database.query(User).filter(User.id == token.user_id).one_or_none()
    return {'user': user.get_filtered_data()}


@router.post('/signup', name='user:create')
def create_user(user: UserCreateForm = Body(..., embed=True), database=Depends(connect_db)):
    exists_user = database.query(User.id).filter(User.email == user.email).one_or_none()
    if exists_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already taken',
        )

    new_user = User(
        email=user.email,
        password=get_password_hash(user.password),
        login=user.login
    )
    database.add(new_user)
    database.commit()
    return {'user_id': new_user.id}
#
#
# @router.get('/stream', name='stream:get')
# def get_stream(token: AuthToken = Depends(check_auth_token), database=Depends(connect_db)):
#     streams_list = database.query(Stream).filter(Stream.user_id == token.user_id).all()
#     return streams_list
#
#
# @router.post('/stream', name='stream:create')
# def create_stream(
#         token: AuthToken = Depends(check_auth_token),
#         stream_form: StreamForm = Body(..., embed=True),
#         database=Depends(connect_db)
# ):
#     stream = Stream(user_id=token.user_id, title=stream_form.title, topic=stream_form.topic,
#                     description=stream_form.description)
#     database.add(stream)
#     database.commit()
#     return {'status': 'created'}
#
#
# @router.put('/stream', name='stream:update')
# def update_stream(
#         token: AuthToken = Depends(check_auth_token),
#         stream_form: StreamUpdateForm = Body(..., embed=True),
#         database=Depends(connect_db)
# ):
#     """
#     Change stream status: active or closed
#     """
#     if stream_form.status not in (StreamStatus.ACTIVE.value, StreamStatus.CLOSED.value):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail='Status must be active or closed',
#         )
#
#     stream = database.query(Stream).filter(Stream.id == stream_form.stream_id,
#                                            Stream.user_id == token.user_id).one_or_none()
#     if not stream:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f'Stream with id {stream_form.stream_id} doesnt exist',
#         )
#
#     stream.status = stream_form.status
#     database.add(stream)
#     database.commit()
#     return {'status': stream_form.status}
