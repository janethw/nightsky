import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

# from flaskr.db import get_db
from flaskr.models import User
from . import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # db.execute(
                #     "INSERT INTO user (username, password) VALUES (?, ?)",
                #     (username, generate_password_hash(password)),
                # )
                user = User(
                    username=username,
                    password=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                db.session.rollback()
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # db = get_db()
        error = None
        # user = db.execute(
        #     'SELECT * FROM user WHERE username = ?', (username,)
        # ).fetchone()

        user = db.session.scalars(db.select(User).where(User.username == username)).one_or_none()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    # this stores g.user as an ORM object, so becomes later accessed by eg, g.user.id
    else:
        # g.user = get_db().execute(
        #     'SELECT * FROM user WHERE id = ?', (user_id,)
        # ).fetchone()
        g.user = db.session.scalars(db.select(User).where(User.id == user_id)).one_or_none()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# Decorator to check user is logged in before editing blog posts
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view