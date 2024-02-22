import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


# The views for auth blueprint:
# views handle the logic for routes
@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        elif not password:
            error = "Password if required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUE (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        # flash() stores the error message where it can be retrieved when rendering the template
        flash(error)

    # handles the GET request, and validation errors:
    return render_template("auth/register.html")
