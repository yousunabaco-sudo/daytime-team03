from flask import Flask, render_template
from .models import db

def create_app():
    app = Flask(__name__)
    from config import Config
    app.config.from_object(Config)

    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
