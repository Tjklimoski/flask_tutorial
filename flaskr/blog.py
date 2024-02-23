from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

# login_required is the decorator function that only allows authenticated users to certain routes
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


# index route, show all of the posts in db
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("blog/index.html", posts=posts)
