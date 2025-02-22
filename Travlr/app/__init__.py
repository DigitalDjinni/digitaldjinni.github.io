from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()  
db_migration = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # App configuration settings
    app.secret_key = '7d19a1ab60e19a371ed4f1c48789dac78d5f3ed5224fb0ac4d8d0100b624924'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ArI#2415@localhost/TravlrDB'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    db_migration.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    login_manager.login_view = 'auth_blueprint.login'

    # Load user from the database
    @login_manager.user_loader
    def load_user(user_id):
        # Importing the User model here to avoid circular imports
        from app.models import User
        return User.query.get(int(user_id))

    # Register Blueprints Routes
    from app.routes.auth_routes import auth_blueprint
    from app.routes.trip_routes import trip_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(trip_blueprint)

    return app
