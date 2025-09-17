from flask import (Blueprint, render_template, request, url_for, redirect, flash, g)
from app.db import get_db
from app.auth import required_auth

bp = Blueprint('todo', __name__, url_prefix='/')

@bp.route('/')
def index():
    return render_template('todo/index.html')

@bp.route('/list')
@required_auth
def list():
    db, c = get_db()
    c.execute('SELECT id, title, description, created_by, completed, created_at FROM todos WHERE created_by = %s', (g.user['id'],))
    todos = c.fetchall()

    return render_template('todo/list.html', todos=todos)

@bp.route('/create', methods=['GET', 'POST'])
@required_auth
def create():
    if request.method == 'POST':
        title = (request.form.get('title') or '').strip()
        description = (request.form.get('description') or '').strip()

        if not title:
            flash('Title is required.', 'error')
            return render_template('todo/create.html', form=request.form), 400
        
        db, c = get_db()

        c.execute('INSERT INTO todos (title, description, created_by) VALUES (%s, %s, %s)', (title, description, g.user['id']))
        db.commit()

        flash('Todo create successfully', 'success')
        return redirect(url_for('todo.list'))

    return render_template('todo/create.html')

@bp.route('/<int:id>/update',  methods=['GET', "POST"])
@required_auth
def update(id):
    db, c = get_db()
    c.execute('SELECT * FROM todos WHERE id = %s AND created_by = %s', (id, g.user['id']))
    todo = c.fetchone()

    if todo is None:
        flash('Todo not found or unauthorized.', 'error')
        return redirect(url_for('todo.list'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        completed = 1 if request.form.get('completed') == '1' else 0
        description = request.form.get('description', '').strip()

        if not title:
            flash('Title is requerid.', 'error')
            return render_template('todo/update.html', todo=todo), 400
        
        c.execute('UPDATE todos SET title = %s, description = %s, completed = %s WHERE id = %s AND created_by = %s ', (title, description, completed, id, g.user['id']))
        db.commit()

        if c.rowcount == 0:
            flash('No changes were made.', 'info')
            return redirect(url_for('todo.list'))

        flash('Todo update successfully.', 'success')
        return redirect(url_for('todo.list'))

    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/detele', methods=['POST'])
@required_auth
def delete(id):
    db, c = get_db()
    c.execute('DELETE FROM todos WHERE id = %s AND created_by = %s', (id, g.user['id']))
    db.commit()

    if c.rowcount == 0:
        flash('Todo not found or unauthorized.', 'error')
    else:
        flash('Todo deleted successfully.', 'success')

    return redirect(url_for('todo.list'))