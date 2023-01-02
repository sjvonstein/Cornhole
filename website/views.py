from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Player, Match, Round, Season
from datetime import datetime
from . import db    # Import database


views = Blueprint("views", __name__)

# Create a route decorator to tell Flask what URL should trigger our function.

# Home Page
@views.route("/")
def home():
    return render_template("home.html")

#------------------- Players -------------------
# Players Page
@views.route("/players", methods=["GET", "POST"])

# Create a function to handle the request when someone goes to /players
def player():
    # Check if the request method is POST (they clicked a submit button)
    if request.method == "POST":
        # Check if the button clicked was the 'addPlayer' button
        if 'addPlayer' in request.form:
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
                return redirect(url_for("views.player"))

        # Check if the button clicked was the 'setDefaults' button
        elif 'setDefaults' in request.form:
            defaultPlayers = ['Jason','Heather','Ethan','Stefanie','Henry','Stefan','Mimi','PopPop']
            for player in defaultPlayers:
                if Player.query.filter_by(first_name=player).first():
                    pass
                else:
                    # Add user to database
                    new_player = Player(first_name=player)
                    db.session.add(new_player)
            db.session.commit()
            return redirect(url_for("views.player"))
    else:
        # If the request method is GET, just render the page
        # Query the database for all players
        players = Player.query.all()

        # Render the players.html template and pass it the players variable
        return render_template("players.html", players=players)

# Delete Player called from players.html
@views.post('/<int:player_id>/delete/') 
def delete_player(player_id):
    player = Player.query.filter_by(id=player_id).first()
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('views.player'))


#------------------- Score Keeper -------------------

@views.route("/score-keeper", methods=["GET", "POST"])

def score_keeper():
    match = Match.query.filter_by(completed=False).first()
    # If there is no match in progress, redirect to matches page
    if match is None:
        flash ("No matches have been started yet. Create a new match first.", category="error")
        return redirect(url_for("views.matches"))
    else:
        rounds = Round.query.filter_by(match_id=match.id).all()
        players = {player.id: player.first_name for player in Player.query.all()}
        player1_total = sum(round.player1_score for round in rounds)
        player2_total = sum(round.player2_score for round in rounds)
        # Alert the user if either player scores at least 21 and there is no tie
        if player1_total >= 21 and player1_total > player2_total:
            flash (players[match.player1] + " Wins!", category="success")
            
            # Complete the match by making a request to the complete_match route
            return redirect(url_for("views.complete_match", match_id=match.id))

        elif player2_total >= 21 and player2_total > player1_total:
            flash (players[match.player2] + " Wins!", category="success")

            # Complete the match by making a request to the complete_match route
            return redirect(url_for("views.complete_match", match_id=match.id))



        return render_template("score-keeper.html", players=players,match=match, rounds=rounds, player1_total=player1_total, player2_total=player2_total)









#------------------- Score Board -------------------

@views.route("/score-board", methods=["GET", "POST"])

def score_board():
    match = Match.query.filter_by(completed=False).first()
    if match is None:
        match=Match.query.order_by(Match.id.desc()).first()
        if match is None:
            flash ("No matches have been started yet. Create a new match first.", category="error")
            return redirect(url_for("views.matches"))
        else:
            return previous_rounds(match.id)
    else:
        rounds = Round.query.filter_by(match_id=match.id).all()
        players = {player.id: player.first_name for player in Player.query.all()}
        player1_total = sum(round.player1_score for round in rounds)
        player2_total = sum(round.player2_score for round in rounds)
        return render_template("score-board.html", players=players,match=match, rounds=rounds, player1_total=player1_total, player2_total=player2_total)


@views.post('/<int:match_id>/previousRounds/')
def previous_rounds(match_id):
    match = Match.query.filter_by(id=match_id).first()
    rounds = Round.query.filter_by(match_id=match.id).all()
    players = {player.id: player.first_name for player in Player.query.all()}
    player1_total = sum(round.player1_score for round in rounds)
    player2_total = sum(round.player2_score for round in rounds)
    return render_template("score-board.html", match=match, rounds=rounds, players=players, player1_total=player1_total, player2_total=player2_total)

@views.post('/<int:match_id>/addRound/') 
def add_round(match_id):
    player1_score = request.form.get("player1_score")
    player2_score = request.form.get("player2_score")
    number = Round.query.filter_by(match_id=match_id).count() + 1
    new_round = Round(match_id=match_id, number=number, player1_score=player1_score, player2_score=player2_score)
    db.session.add(new_round)
    db.session.commit()
    return redirect(url_for('views.score_keeper'))





@views.route("/seasons", methods=["GET", "POST"])
def add_season():
    if request.method == "POST":
        name = request.form.get("name")
        startDate = request.form.get("startDate")
        if Season.query.filter_by(closed=False).count() >0:
            flash("Season already in progress", category="error")
        elif len(name) < 2:
            flash("Name must be greater than 1 characters", category="error")
        elif Season.query.filter_by(name=name).first():
            flash("Name already exists", category="error")
        else:
            # Add season to database
            new_season = Season(name=name, startDate=datetime.strptime(startDate, '%Y-%m-%d'))
            db.session.add(new_season)
            db.session.commit()
            flash("Season Created.", category="success")
            return redirect(url_for("views.add_season"))

    seasons = Season.query.all()
    return render_template("seasons.html", seasons=seasons)

@views.post('/<int:season_id>/deleteSeason/') 
def delete_season(season_id):
    season = Season.query.filter_by(id=season_id).first()
    matches = Match.query.filter_by(season=season_id).all()
    for match in matches:
        rounds = Round.query.filter_by(match_id=match.id).all()
        for round in rounds:
            db.session.delete(round)
        db.session.delete(match)
    db.session.delete(season)
    db.session.commit()
    return redirect(url_for('views.add_season'))

#Route to close a season
@views.post('/<int:season_id>/closeSeason/')
def close_season(season_id):
    season = Season.query.filter_by(id=season_id).first()
    season.closed = True
    db.session.commit()
    return redirect(url_for('views.add_season'))

#Route to open a season, only if there is no other open season
@views.post('/<int:season_id>/openSeason/')
def open_season(season_id):
    season = Season.query.filter_by(id=season_id).first()
    if Season.query.filter_by(closed=False).count() >0:
        flash("Season already in progress", category="error")
    else:
        season.closed = False
        db.session.commit()
    return redirect(url_for('views.add_season'))

#-------------------Matches-------------------

@views.route("/matches", methods=["GET", "POST"])
def matches():
    
    if request.method == "POST":
        season_id = request.form.get("seasonSelect")
        player1_id = request.form.get("player1Select")
        player2_id = request.form.get("player2Select")
        
        if not season_id or not player1_id or not player2_id:
            flash("Please select a season, player 1 and player 2", category="error")
        elif Match.query.filter_by(completed=False).count() >0:
            flash("Match already in progress", category="error")
        elif player1_id == player2_id:
            flash("Players must be different", category="error")
        else:
            # Add match to database
            new_match = Match(season=season_id, player1=player1_id, player2=player2_id, completed=False)
            db.session.add(new_match)
            db.session.commit()
            flash("Match Created.", category="success")
            return redirect(url_for('views.score_keeper'))

    openSeasons = Season.query.filter_by(closed=False)
    seasons = {season.id: season.name for season in Season.query.all()}
    allPlayers = Player.query.all()
    matches = Match.query.all()
    players = {player.id: player.first_name for player in Player.query.all()}
    return render_template("matches.html", matches=matches, players=players, allPlayers=allPlayers, seasons=seasons, openSeasons=openSeasons)

@views.post('/<int:match_id>/deleteMatch/') 
def delete_match(match_id):
    match = Match.query.filter_by(id=match_id).first()
    Round.query.filter_by(match_id=match.id).delete()
    db.session.delete(match)
    db.session.commit()
    return redirect(url_for('views.matches'))

@views.route('/<int:match_id>/completeMatch/', methods=["GET", "POST"]) 
def complete_match(match_id):
    match = Match.query.filter_by(id=match_id).first()
    rounds = Round.query.filter_by(match_id=match.id).all()
    if len(rounds) < 3:
        flash("Match must have at least 3 rounds", category="error")
        return redirect(url_for('views.matches'))
    else:
        # Total scores for each player
        player1_total = 0
        player2_total = 0
        for round in rounds:
            player1_total += round.player1_score
            player2_total += round.player2_score
        # Check if there was a tie and return an error is true
        if player1_total == player2_total:
            flash("Match cannot end in a tie", category="error")
            return redirect(url_for('views.matches'))
        # Check that either player scored at least 21 points
        elif player1_total < 21 and player2_total < 21:
            flash("Match must have at least 21 points", category="error")
            return redirect(url_for('views.matches'))
        else: 
            # Add the scores to the match record
            match.player1_score = player1_total
            match.player2_score = player2_total
            match.completed = True
            db.session.commit()
            return redirect(url_for('views.matches'))

@views.post('/<int:match_id>/openMatch/') 
def open_match(match_id):
    if Match.query.filter_by(completed=False).count() >0:
        flash("Match already in progress", category="error")
        return redirect(url_for('views.matches'))
    else:
        match = Match.query.filter_by(id=match_id).first()
        match.completed = False
        db.session.commit()
        return redirect(url_for('views.matches'))



# --------------- ROUNDS -----------------
@views.route("/rounds", methods=["GET", "POST"])
def rounds():

    return render_template("rounds.html")


@views.post('/<int:round_id>/deleteRound/') 
def delete_round(round_id):
    round = Round.query.filter_by(id=round_id).first()
    db.session.delete(round)
    db.session.commit()
    return redirect(url_for('views.score_keeper'))


# --------------- STATISTICS -----------------
@views.route("/stats", methods=["GET", "POST"])
def statistics():

    return render_template("statistics.html")