
from . import db
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("player.id"))

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), unique=True)
    notes = db.relationship("Note")


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    startDate = db.Column(db.DateTime(timezone=True), default=func.now())
    endDate = db.Column(db.DateTime(timezone=True), default=func.now())
    closed = db.Column(db.Boolean, default=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2 = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player1_score = db.Column(db.Integer, nullable=False)
    player2_score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    season = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)

class Round(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match= db.Column(db.Integer, db.ForeignKey('match.id'), nullable=False)
    player1_score = db.Column(db.Integer, nullable=False)
    player2_score = db.Column(db.Integer, nullable=False)