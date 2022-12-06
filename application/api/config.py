import os

# configuraciones. True para que el servidor pueda ser levantado en modo debug
DEBUG = True

# configuracion BD

POSTGRES = {
    "user": "postgres",
    "pw": "master",
    "db": "idatos2022",
    "host": "localhost",
    "port": "5432",
}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:master@localhost:5432/idatos2022"
