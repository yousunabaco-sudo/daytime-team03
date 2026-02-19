from flask import render_template, redirect, url_for, flash, request
from app.blueprints.admin import admin_bp
from flask_login import login_required, current_user
from app.models import Post, Category, User, db

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    post_count = Post.query.count()
    user_count = User.query.count()
    return render_template('admin/dashboard.html', title='管理画面', posts=posts, post_count=post_count, user_count=user_count)

@admin_bp.route('/posts')
@login_required
def post_list():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/post_list.html', title='記事管理', posts=posts)

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
    users = User.query.all()
    return render_template('admin/admin_users.html', users=users, active_menu='user_list')

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
