from flask import render_template, request, url_for
from app.blueprints.main import main_bp
from app.models import Post, Category
from datetime import datetime, timedelta
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None


def _now_jst():
    """日本時間の現在時刻（naive、published_at と比較用）"""
    if ZoneInfo:
        return datetime.now(ZoneInfo('Asia/Tokyo')).replace(tzinfo=None)
    return datetime.utcnow() + timedelta(hours=9)


@main_bp.route('/')
@main_bp.route('/index')
def index():
    now_jst = _now_jst()
    # Topics (Category: topics)
    topics_category = Category.query.filter_by(slug='topics').first()
    topics_posts = []
    if topics_category:
        topics_posts = Post.query.filter(
            Post.category_id == topics_category.id,
            Post.published_at <= now_jst
        ).order_by(Post.published_at.desc()).limit(5).all()

    # Events (Category: event)
    event_category = Category.query.filter_by(slug='event').first()
    event_posts = []
    if event_category:
        event_posts = Post.query.filter(
            Post.category_id == event_category.id,
            Post.published_at <= now_jst
        ).order_by(Post.published_at.desc()).limit(2).all()

    return render_template('main/index.html', title='ホーム', 
                         posts=topics_posts, # Backward compatibility for base.html if needed, or primarily for topics section
                         topics_posts=topics_posts,
                         event_posts=event_posts)

@main_bp.route('/blog')
def blog_list():
    page = request.args.get('page', 1, type=int)
    category_slug = request.args.get('category')
    now_jst = _now_jst()
    query = Post.query.filter(Post.published_at <= now_jst)
    current_category = None
    
    if category_slug:
        current_category = Category.query.filter_by(slug=category_slug).first()
        if current_category:
            query = query.filter_by(category_id=current_category.id)
            
    pagination = query.order_by(Post.published_at.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = pagination.items
    categories = Category.query.all()
    
    return render_template('main/blog_list.html', 
                         title='ブログ記事一覧', 
                         posts=posts, 
                         pagination=pagination, 
                         categories=categories,
                         current_category=current_category)

@main_bp.route('/blog/detail/<int:id>')
def blog_detail(id):
    post = Post.query.get_or_404(id)
    now_jst = _now_jst()
    # サイドバー用データ
    categories = Category.query.all()
    recent_posts = Post.query.filter(Post.published_at <= now_jst).order_by(Post.published_at.desc()).limit(5).all()

    return render_template('main/blog_detail.html', 
                         post=post,
                         categories=categories,
                         recent_posts=recent_posts)

@main_bp.route('/essay')
def essay_list():
    return render_template('main/essay_list.html', title='エッセー・書評')

@main_bp.route('/event')
def event_list():
    return render_template('main/event_list.html', title='勉強会・セミナー')
