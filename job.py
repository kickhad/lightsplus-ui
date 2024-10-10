from sqlalchemy import create_engine, Column, Integer, String, Boolean, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import paho.mqtt.publish as publish
import time
from config import Config
from lpui.models import Update


# MQTT broker configuration


# SQLAlchemy setup
engine = create_engine("sqlite:///instance/lpui.db")
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
        publish.single('lightsplus-20241007/a2', leds, hostname='test.mosquitto.org')

        # Update the record to complete = True
        record.published = True
        session.commit()


    session.close()

# Main loop to run every 3 seconds
if __name__ == "__main__":
    while True:
        check_and_send_update()
        time.sleep(3)