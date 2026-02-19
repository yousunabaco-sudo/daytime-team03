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

    @app.route('/blog/detail')
    def blog_detail():
        return render_template('blog_detail.html')

    @app.route('/admin')
    def admin_login():
        return render_template('admin_login.html')

    @app.route('/admin/users')
    def admin_users():
        return render_template('admin_users.html')

    @app.route('/admin/users/new')
    def admin_user_new():
        return render_template('admin_user_new.html')

    return app
