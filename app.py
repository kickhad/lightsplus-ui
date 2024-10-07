from flask import Flask, jsonify, request, render_template, redirect, url_for
from data import board_games
import threading
import time

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)