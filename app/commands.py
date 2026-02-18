import click
from flask.cli import with_appcontext
from app import db
from app.models import User, Category

@click.command('seed-db')
@with_appcontext
def seed_db():
    """初期データの投入"""
    # 既存データの削除（必要に応じて）
    # Category.query.delete()
    
    # カテゴリーの作成
    categories = [
        {'name': 'エッセー', 'slug': 'essay'},
        {'name': '書評', 'slug': 'book-review'},
        {'name': 'イベント告知', 'slug': 'event'},
        {'name': 'お知らせ', 'slug': 'news'}
    ]
    for cat_data in categories:
        if not Category.query.filter_by(slug=cat_data['slug']).first():
            cat = Category(name=cat_data['name'], slug=cat_data['slug'])
            db.session.add(cat)
    
    # 管理者ユーザーの作成
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(name='管理者', email='admin@example.com', role='admin')
        admin.set_password('password123')
        db.session.add(admin)
    
    db.session.commit()
    click.echo('初期データの投入が完了しました。')

def init_app(app):
    app.cli.add_command(seed_db)
