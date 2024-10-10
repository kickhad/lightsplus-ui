from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_mqtt import Mqtt
from flask_cors import CORS
db = SQLAlchemy()

cors = CORS()
mqtt = Mqtt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    cors.init_app(app, origins="*", allow_headers=["Content-Type"], methods=["GET", "POST"])
    mqtt.init_app(app, threaded=True)
    from .routes import main
    app.register_blueprint(main)

    return app