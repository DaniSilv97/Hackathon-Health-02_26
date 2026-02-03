from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config.database import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)

    # Register routes
    from app.routes.web import web_bp
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp

    app.register_blueprint(web_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Create tables
    with app.app_context():
        from app.models.user import User
        db.create_all()

    # Register CLI commands
    from database.commands import register_commands
    register_commands(app)

    return app
