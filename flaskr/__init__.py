# a __init__.py file in a folder tells python to treat that folder as a package / module.
# To have vscode recognize the imports in the venv, make sure to set the Python Interpreter to the venv
import os

from flask import Flask


# create_app is the application factory
def create_app(test_config=None):
    # create and configure the app

    # Flask() creates the instance,
    # __name__ is the name of current Python module (in order for flask to setup paths)
    # instance_relative_config tells flask if the config files are relative to the instance folder.
    app = Flask(__name__, instance_relative_config=True)

    # sets default config
    app.config.from_mapping(
        # keeps data safe, set to more complex string when deploying
        SECRET_KEY="dev",
        # path to database location. we'll be using SQLite
        # app.instance_path is the instance folder flask creates
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # will overide the default config (above) if config.py exists in instance folder.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        # Allows your test to be configured independently to any dev values.
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists, flask doesn't create the doler automatically
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Initalize database
    from . import db

    db.init_app(app)

    # Register auth blueprint with app
    from . import auth

    app.register_blueprint(auth.bp)

    from . import blog

    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
