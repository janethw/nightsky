from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

import requests

bp = Blueprint('apod', __name__)


@bp.route('/apod')
def apod():
    try:
        api_key = current_app.config['API_KEY']
        url_gallery = f"https://api.nasa.gov/planetary/apod?count=10&api_key={api_key}"
        url_apod = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"
        response_gallery = requests.get(url_gallery)
        response_apod = requests.get(url_apod)
        if response_gallery.status_code == 200 & response_apod.status_code == 200:
            apod_today = response_apod.json()
            apod_today_image = apod_today['url']
            apod_today_title = apod_today['title']
            apod_images = response_gallery.json()
            image_urls = [image['url'] for image in apod_images]
            titles = [image['title'] for image in apod_images]
            return render_template('apod/apod_index.html', image_urls=image_urls, titles=titles, arr_len=len(titles), apod_today_image=apod_today_image, apod_today_title=apod_today_title)
        else:
            return f"Error - unable to fetch data. {response_gallery.status_code}, {response_apod.status_code}", 500
    except Exception as e:
        return f"Error occurred: {e}", 500


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')


# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))