from . import db

class BoardGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_game_name = db.Column(db.String(128), nullable=False)
    minimum_players = db.Column(db.Integer, nullable=False)
    maximum_players = db.Column(db.Integer, nullable=False)
    first_led = db.Column(db.Integer, nullable=False)
    last_led = db.Column(db.Integer, nullable=False)

    categories = db.relationship('Category', secondary='board_game_category', backref=db.backref('board_games', lazy='dynamic'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(128), nullable=False, unique=True)

class BoardGameCategory(db.Model):
    board_game_id = db.Column(db.Integer, db.ForeignKey('board_game.id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)

class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    leds = db.Column(db.String)
    published = db.Column(db.Boolean)
    