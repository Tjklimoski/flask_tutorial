from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from werkzeug.exceptions import abort

# login_required is the decorator function that only allows authenticated users to certain routes
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)
