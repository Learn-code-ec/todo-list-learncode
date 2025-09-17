import functools
from flask import (Blueprint, render_template, request, flash, redirect, url_for, session, g)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()

        if not username:
            flash('Username is required.', 'error')
            return render_template('auth/register.html', form=request.form), 400
        
        if not password or len(password) < 6:
            flash('Password is required and must contains at least 6 characters.', 'error')
            return render_template('auth/register.html', form=request.form), 400
        
        db, c = get_db()

        c.execute('SELECT id FROM users WHERE username = %s', (username,))
        user = c.fetchone()

        if user:
            flash('Username already exist.', 'error')
            return render_template('auth/register.html', form=request.form), 409
        
        c.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, generate_password_hash(password)))
        db.commit()
    
        flash('User registered successfully, you can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = (request.form.get('username') or '').strip()
        password = (request.form.get('password') or '').strip()

        if not username:
            flash('Username is required.', 'error')
            return render_template('auth/login.html'), 400
        
        if not password or len(password) < 6:
            flash('password is required and must contain at least 6 characters.', 'error')
            return render_template('auth/login.html'), 400
        
        db, c = get_db()

        c.execute('SELECT id, username, password FROM users WHERE username = %s', (username,))
        user = c.fetchone()

        if not user:
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html'), 401

        if not check_password_hash(user['password'], password):
            flash('invalid username or password.', 'error')
            return render_template('auth/login.html'), 401
        
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('todo.index'))
        
    return render_template('auth/login.html')

@bp.before_app_request
def load_in_logger_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else: 
        db, c = get_db()
        c.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        g.user = c.fetchone()


def required_auth(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    
    return wrapped_view

@bp.route('/logout')
@required_auth
def logout():
    session.clear()
    return redirect(url_for('todo.index'))