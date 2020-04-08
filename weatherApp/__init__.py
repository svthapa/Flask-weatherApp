from flask import Flask
from .weatherApp import db

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key='asdjnasdnasndsdas'


    app.config['DEBUG'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pccwvjvplvkbyc:cf11d9ede7ef9995c8d553a99a1cecfc4e83bf303ea6ddec4c8da7bdf3979cdc@ec2-52-200-119-0.compute-1.amazonaws.com:5432/dagl2v5ed546h8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.init_app(app)


    from .weatherApp import bp
    app.register_blueprint(bp)

    return app
