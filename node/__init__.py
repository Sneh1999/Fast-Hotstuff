import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ["SECRET_KEY"],
        DATABASE=os.environ["NODE_ID"] +
        os.environ['FLASK_RUN_PORT'] + ".sqlite"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():
        return 'Node started'

    @app.route('/status')
    def status():
        return {
            "host": request.remote_addr,
            "port":  os.environ['FLASK_RUN_PORT'],
            "node_id": os.environ["NODE_ID"]
        }
    return app
