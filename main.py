from fastapi import FastAPI
from app.config import config, engine, Base
from app.handlers import router
from app import handlersauth, handlerscalc
from fastapi.staticfiles import StaticFiles

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
