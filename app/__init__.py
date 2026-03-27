from flask import Flask
from flasgger import Swagger
from .extensions import db, migrate, jwt
from .config import Config
from .routes import register_routes
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    swagger = Swagger(app)  # 👈 muda pra essa forma

    print(app.url_map)  # 👈 DEBUG (MUITO IMPORTANTE)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    register_routes(app)

    return app