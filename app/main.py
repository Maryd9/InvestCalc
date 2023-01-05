from fastapi import FastAPI
from app.config import DEBUG, PROJECT_NAME, VERSION
from app.handlers import router
import uvicorn
from app.settings import settings


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.include_router(router)
    return application


# Активация виртуального окружения venv/Scripts/activate
# Деактивация deactivate
# Запуск приложения uvicorn app.main:app
app = get_application()

# создаем объект database, который будет использоваться для выполнения запросов
# database = databases.Database(DATABASE_URL)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.server_host, port=settings.server_port, reload=True)
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
