from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
# from flaskr.db import get_db

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


@bp.route('/gallery')
def gallery():
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
            return render_template('apod/apod_gallery.html', image_urls=image_urls, titles=titles, arr_len=len(titles), apod_today_image=apod_today_image, apod_today_title=apod_today_title)
        else:
            return f"Error - unable to fetch data. {response_gallery.status_code}, {response_apod.status_code}", 500
    except Exception as e:
        return f"Error occurred: {e}", 500
