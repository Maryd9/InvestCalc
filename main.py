import uvicorn
from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import config, engine, Base
from app.handlers import router, RequiresLoginException
from app import handlersauth, handlerscalc
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import Response

from app.settings import settings
from starlette.responses import RedirectResponse

API_PREFIX = '/api'
VERSION = '0.0.1'
DEBUG = config('DEBUG', cast=bool, default=False)
PROJECT_NAME = config('PROJECT_NAME', default='InvestCalc App Api')


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(router)
    application.include_router(handlersauth.router)
    application.include_router(handlerscalc.router)
    return application


app = get_application()

# создаем таблицы для бд
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(SessionMiddleware, secret_key="some-random-string")


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return RedirectResponse(url='/')


@app.middleware("http")
async def create_auth_header(request: Request, call_next):
    #     request: Request,
    #     call_next, ):
    # if ("Authorization" not in request.headers
    #         and "Authorization" in request.cookies
    # ):
    #     access_token = request.cookies["Authorization"]
    #
    #     request.headers.__dict__["_list"].append(
    #         (
    #             "authorization".encode(),
    #             f"Bearer {access_token}".encode(),
    #         )
    #     )
    # elif ("Authorization" not in request.headers
    #       and "Authorization" not in request.cookies
    # ):
    #     request.headers.__dict__["_list"].append(
    #         (
    #             "authorization".encode(),
    #             f"Bearer 12345".encode(),
    #         )
    #     )

    response = await call_next(request)
    session = request.cookies.get('session')
    if session:
        response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True)
    return response


if __name__ == "__main__":
    uvicorn.run('main.py', host=settings.settings.server_host, port=settings.settings.server_port, reload=True)
