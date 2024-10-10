from sqlalchemy import create_engine, Column, Integer, String, Boolean, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import paho.mqtt.client as mqtt
import time
from config import Config
from lpui.models import Update


# MQTT broker configuration
mqtt_broker = Config.MQTT_BROKER_URL
mqtt_port = Config.MQTT_BROKER_PORT
mqtt_topic = Config.MQTT_TOPIC

# SQLAlchemy setup
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)



# Function to check for the most recent record and send to MQTT
def check_and_send_update():
    session = Session()
    query = select(Update).where(Update.leds.isnot(None), Update.published == False).order_by(Update.id.desc()).limit(1)
    record = session.execute(query).scalar()

    if record:
        leds = record.leds
        print(f"Found new update: {leds}")
        # Send to MQTT
        mqtt.publish.single(Config.MQTT_TOPIC, leds)        

        # Update the record to complete = True
        record.published = True
        session.commit()


    session.close()

# Main loop to run every 3 seconds
if __name__ == "__main__":
    while True:
        check_and_send_update()
        time.sleep(3)