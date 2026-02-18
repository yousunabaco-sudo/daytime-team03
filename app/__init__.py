from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def index():
        return "Hello, World! (Project Reset)"

    return app
