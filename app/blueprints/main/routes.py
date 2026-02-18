from flask import render_template
from app.blueprints.main import main_bp
from app.models import Post

@main_bp.route('/')
@main_bp.route('/index')
def index():
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).limit(5).all()
    return render_template('main/index.html', title='ホーム', posts=posts)

@main_bp.route('/essay')
def essay_list():
    return render_template('main/essay_list.html', title='エッセー・書評')

@main_bp.route('/event')
def event_list():
    return render_template('main/event_list.html', title='勉強会・セミナー')
