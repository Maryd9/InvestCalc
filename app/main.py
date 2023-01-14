from deta import Deta
from fastapi import FastAPI
from app.config import DEBUG, PROJECT_NAME, VERSION
from app.handlers import router
from app import handlersauth, handlerscalc
from fastapi.staticfiles import StaticFiles


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(router)
    application.include_router(handlersauth.router)
    application.include_router(handlerscalc.router)
    return application


# Активация виртуального окружения .venv/Scripts/activate
# Деактивация deactivate
# Запуск приложения uvicorn app.main:app
app = get_application()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

deta = Deta("project key")
