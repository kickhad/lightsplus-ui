from flask import Blueprint, jsonify, request
from . import db
from .models import BoardGame, Category

main = Blueprint('main', __name__)

@main.route('/filter', methods=['GET'])
def filter_board_games(category_ids=None, player_count=None):
    if category_ids is None:
        category_ids = request.args.getlist('category_ids', type=int)
    if player_count is None:
        player_count = request.args.get('player_count', type=int)

    query = BoardGame.query

    if category_ids:
        query = query.join(BoardGame.categories).filter(Category.id.in_(category_ids))

    if player_count:
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