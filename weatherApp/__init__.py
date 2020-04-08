from flask import Flask
from .weatherApp import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key='asdjnasdnasndsdas'
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gasbt435@localhost/weatherapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)


    from .weatherApp import bp
    app.register_blueprint(bp)

    return app
