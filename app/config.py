# app/config.py
import os


class Config:
    MYSQL_HOST = os.environ.get("DB_HOST", "localhost")
    MYSQL_USER = os.environ.get("DB_USER", "root")
    MYSQL_PASSWORD = os.environ.get("DB_PASS", "asd123")
    MYSQL_DB = os.environ.get("DB_NAME", "todo_db")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "somesecretkey")
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
