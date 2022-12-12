from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Player, Match, Round, Season
from . import db    # Import database


views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/players", methods=["GET", "POST"])
def add_player():
    if request.method == "POST":
        first_name = request.form.get("firstName")
        if len(first_name) < 2:
            flash("Name must be greater than 1 characters", category="error")
        elif Player.query.filter_by(first_name=first_name).first():
            flash("Name already exists", category="error")
        else:
            # Add user to database
            new_player = Player(first_name=first_name)
            db.session.add(new_player)
            db.session.commit()
            flash("Player Created.", category="success")  # Display success message
            return redirect(url_for("views.add_player"))  

    players = Player.query.all()
    return render_template("players.html", players=players)

@views.post('/<int:player_id>/delete/') 
def delete_player(player_id):
    player = Player.query.filter_by(id=player_id).first()
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('views.add_player'))


@views.route("/score-board", methods=["GET", "POST"])
def score_board():
    players = Player.query.all()
    return render_template("score-board.html", players=players)