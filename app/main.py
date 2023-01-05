from fastapi import FastAPI
from app.config import API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.handlers import router


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(router, prefix=API_PREFIX)
    return application


# Активация виртуального окружения venv/Scripts/activate
# Деактивация deactivate
# Запуск приложения uvicorn app.main:app
app = get_application()

# создаем объект database, который будет использоваться для выполнения запросов
# database = databases.Database(DATABASE_URL)


# @app.on_event("startup")
# async def startup():
#     # когда приложение запускается устанавливаем соединение с БД
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     # когда приложение останавливается разрываем соединение с БД
#     await database.disconnect()
