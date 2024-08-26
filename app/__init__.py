# app/__init__.py
from flask import Flask
from app.config import config
from app.extensions import mysql
from app.routes import todo_bp, seeder_bp

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    mysql.init_app(app)
    
    # Register blueprints
    app.register_blueprint(todo_bp)
    app.register_blueprint(seeder_bp)
    
    return app
