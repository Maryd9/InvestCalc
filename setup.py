from setuptools import setup

setup(
    name='app-example',
    version='0.0.1',
    description='InvestCalc app',
    install_requires=[
        'fastapi==0.88.0',
        #Виртуальный сервер
        'uvicorn==0.20.0',
        #ORM, для общения с бд
        'SQLAlchemy==1.4.45',
        'pytest==7.2.0',
        #Для http запросов
        'requests==2.28.1',
    ]
    ,
    scripts=['main.py', 'scripts/create_db.py']
)