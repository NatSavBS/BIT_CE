import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=b'\xd5eR\xd3\xee\xd0\xec(r{\x1f\xe1\xf2G[B',
        DATABASE=os.path.join(app.instance_path, 'CEForm.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import secure
    app.register_blueprint(secure.bp)
    app.add_url_rule('/', endpoint='index')

    return app