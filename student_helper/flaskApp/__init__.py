from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskApp.admin.routes import ad
    from flaskApp.materials.routes import mat
    from flaskApp.queue.routes import que
    from flaskApp.index_info.routes import ii
    app.register_blueprint(ad)
    app.register_blueprint(mat)
    app.register_blueprint(que)
    app.register_blueprint(ii)

    return app