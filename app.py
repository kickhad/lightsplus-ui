from flask import Flask, jsonify, request, render_template, redirect, url_for
import itertools
from data import board_games
import threading
import time
import json
# from mqtt_client import create_mqtt_client
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'test.mosquitto.org'  # Use the MQTT broker URL
app.config['MQTT_BROKER_PORT'] = 1883  # Default MQTT port
app.config['MQTT_USERNAME'] = ''  # Optional: Set this if you need username/password
app.config['MQTT_PASSWORD'] = ''  # Optional: Set this if you need username/password
app.config['MQTT_KEEPALIVE'] = 5  # Set the KeepAlive time in seconds
app.config['MQTT_TLS_ENABLED'] = False  # Set to True if using TLS, False otherwise

# mqtt_client = create_mqtt_client(app)
mqtt = Mqtt(app)
# Initialize the selected games as an empty list
selected_games = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display')
def display():
    return render_template('display.html')

@app.route('/api/boardgames', methods=['GET'])
def get_board_games():
    return jsonify(board_games)

@app.route('/api/selected-games', methods=['POST'])
def receive_selected_games():
    global selected_games
    selected_games = request.json
    merged = list(itertools.chain.from_iterable(range(game['FirstLED'], game['LastLED']) for game in board_games))
    mqtt.publish('lightsplus-20241007/a1',','.join([f'{f}' for f in merged]))
    return jsonify({"status": "success"})

@app.route('/api/led-data', methods=['GET'])
def get_led_data():
    global selected_games
    led_indices = []

    for game in selected_games:
        led_indices.extend(range(game['FirstLED'], game['LastLED'] + 1))

    return jsonify({'ledIndices': led_indices})

def periodic_refresh():
    while True:
        time.sleep(5)  # Refresh every 5 seconds
        with app.test_request_context():
            led_data = get_led_data()
            with open('led_data.json', 'w') as f:
                f.write(led_data.get_data(as_text=True))

# Start the periodic refresh in a separate thread
threading.Thread(target=periodic_refresh, daemon=True).start()

@app.route('/publish')
def publish():
    # mqtt_client.publish('test/topic', 'Hello MQTT')  # Publish a message to a topic
    return "Message published"

if __name__ == '__main__':
    app.run(debug=True)