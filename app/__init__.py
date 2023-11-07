from flask import Flask

from flask_login import LoginManager

from config import Config
from app.extensions import db, ma
from app.models import User, Game


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    ma.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.game import bp as game_bp
    app.register_blueprint(game_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    return app
