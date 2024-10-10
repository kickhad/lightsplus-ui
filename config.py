PROD = False


class Config:

    if PROD:
        pass # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://kickhad:whattheepicfuck6789@kickhad.mysql.pythonanywhere-services.com:3306/kickhad$lpui"
    else:
        pass
    SQLALCHEMY_DATABASE_URI = "sqlite:///lpui.db"
    SECRET_KEY = "development key"
    USERNAME = "admin"
    PASSWORD = "default"

    # MQTT configuration
    MQTT_BROKER_URL = "test.mosquitto.org"  # Use the MQTT broker URL
    MQTT_BROKER_PORT = 1883  # Default MQTT port
    MQTT_USERNAME = ""  # Optional: Set this if you need username/password
    MQTT_PASSWORD = ""  # Optional: Set this if you need username/password
    MQTT_KEEPALIVE = 5  # Set the KeepAlive time in seconds
    MQTT_TLS_ENABLED = False  # Set to True if using TLS, False otherwise
    MQTT_TOPIC = 'lightsplus-20241007/a2'