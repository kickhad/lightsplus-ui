from flask import Blueprint, jsonify, request, render_template
from . import db, mqtt
from .models import BoardGame, Category
import json

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/filter', methods=['GET'])
def filter_board_games():
    category_ids = request.args.getlist('category_ids', type=int)
    player_count = request.args.get('player_count', type=int)

    query = BoardGame.query

    if category_ids:
        query = query.join(BoardGame.categories).filter(Category.id.in_(category_ids))

    if player_count is not None:
        query = query.filter(BoardGame.minimum_players <= player_count, BoardGame.maximum_players >= player_count)

    board_games = query.all()

    return jsonify([{
        'id': bg.id,
        'board_game_name': bg.board_game_name,
        'minimum_players': bg.minimum_players,
        'maximum_players': bg.maximum_players,
        'first_led': bg.first_led,
        'last_led': bg.last_led,
        'categories': [{'id': cat.id, 'category_name': cat.category_name} for cat in bg.categories]
    } for bg in board_games])



@main.route('/data', methods=['GET'])
def board_games_data():
    category_ids = request.args.getlist('category_ids', type=int)
    player_count = request.args.get('player_count', type=int)

    query = BoardGame.query

    board_games = query.all()

    return jsonify([{
        'id': bg.id,
        'board_game_name': bg.board_game_name,
        'minimum_players': bg.minimum_players,
        'maximum_players': bg.maximum_players,
        'first_led': bg.first_led,
        'last_led': bg.last_led,
        'categories': [{'id': cat.id, 'category_name': cat.category_name} for cat in bg.categories]
    } for bg in board_games])

@main.route('/publish', methods=['POST'])
def publish():
    data = request.json
    result = []
    query = BoardGame.query.filter(BoardGame.id.in_(data['board_game_ids']))
    [result.extend(range(i.first_led, i.last_led)) for i in query.all()]


    # data['board_game_ids']

    # board_game_name = data.get('boardGameName')
    # player_count = data.get('playerCount')
    # table_data = data.get('tableData')

    # # Process LED data
    # leds = []
    # for r in table_data:
    #     [leds.append(n) for n in range(r['first_led'], r['last_led'] + 1)]

    # Publish LED data via MQTT
    mqtt.publish('lightsplus-20241007/a2', json.dumps(result))

    # # Here you can process the data as needed, e.g., save it to a file or database
    # print('Received data:', data)
    # print('Board Game Name:', board_game_name)
    # print('Player Count:', player_count)
    # print('Table Data:', table_data)
    # print('LEDs:', leds)

    return jsonify({'message': 'Table state published successfully'})