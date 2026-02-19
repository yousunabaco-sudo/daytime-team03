from flask import render_template, redirect, url_for, flash, request
from app.blueprints.admin import admin_bp
from flask_login import login_required, current_user
from app.models import Post, Category, User, db

@admin_bp.route('/')
@login_required
def index():
    return redirect(url_for('admin.post_list'))

@admin_bp.route('/posts')
@login_required
def post_list():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    
    query = Post.query
    if q:
        query = query.filter(Post.title.contains(q))
    
    pagination = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = pagination.items
    
    return render_template('admin/post_list.html', 
                         title='記事管理', 
                         posts=posts, 
                         pagination=pagination, 
                         q=q)

@admin_bp.route('/posts/new', methods=['GET', 'POST'])
@login_required
def create_post():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category_id = request.form.get('category_id')
        status = request.form.get('status', 'published')
        
        post = Post(title=title, content=content, category_id=category_id, status=status, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('記事を投稿しました。')
        return redirect(url_for('admin.post_list'))
        
    return render_template('admin/post_form.html', title='新規記事投稿', categories=categories)

# --- 会員管理 ---

@admin_bp.route('/users')
@login_required
def admin_users():
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '')
    role = request.args.get('role', '')
    sort = request.args.get('sort', 'newest')
    
    query = User.query
    if q:
        query = query.filter((User.name.contains(q)) | (User.email.contains(q)))
    
    if role:
        query = query.filter(User.role == role)
    
    if sort == 'name_asc':
        query = query.order_by(User.name.asc())
    elif sort == 'name_desc':
        query = query.order_by(User.name.desc())
    else:
        query = query.order_by(User.created_at.desc())
        
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    users = pagination.items
    
    return render_template('admin/admin_users.html', 
                         users=users, 
                         pagination=pagination, 
                         q=q,
                         role=role,
                         sort=sort,
                         active_menu='user_list')

@admin_bp.route('/users/new')
@login_required
def admin_user_new():
    return render_template('admin/admin_user_new.html', active_menu='user_new')

# --- 記事編集・削除 ---

@admin_bp.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.category_id = request.form.get('category_id')
        post.status = request.form.get('status')
        
        db.session.commit()
        flash('記事を更新しました。')
        return redirect(url_for('admin.post_list'))
        
    return render_template('admin/post_form.html', title='記事編集', post=post, categories=categories)

@admin_bp.route('/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('記事を削除しました。')
    return redirect(url_for('admin.post_list'))
