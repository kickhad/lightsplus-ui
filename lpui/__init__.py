from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_mqtt import Mqtt
db = SQLAlchemy()

mqtt = Mqtt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mqtt.init_app(app)
    from .routes import main
    app.register_blueprint(main)

    return app