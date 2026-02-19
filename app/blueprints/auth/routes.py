from flask import render_template, redirect, url_for, flash, request
from app.blueprints.auth import auth_bp
from flask_login import login_user, logout_user, current_user
from app.models import User
from urllib.parse import urlparse

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is None or not user.check_password(request.form.get('password')):
            flash('メールアドレスまたはパスワードが正しくありません。')
            return redirect(url_for('auth.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('admin.dashboard')
        return redirect(next_page)
        
    return render_template('auth/admin_login.html', title='ログイン')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
