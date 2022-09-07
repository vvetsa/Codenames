from flask import Flask, render_template, request, flash
from random import choice, shuffle

from game import *

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route("/grid", methods=["GET", "POST"])
def grid():
    cardtypes = [str(card.cardtype).upper() for card in cards]
    team = current_team
    team2 = other_team(team)
    message = ''
    if request.method == "POST":
        guess = request.form.get("guess")

        if guess == 'pass':
            return team2
    
        card = lookup_card(guess)

        if not card:
            return render_template("grid.html", cards=cards, cardtypes=cardtypes, message='that\'s not one of the words. try again.', team=team)
        
        if card.revealed:
            return render_template("grid.html", cards=cards, cardtypes=cardtypes, message='that card has already been guessed. try again.', team=team)

        card.revealed = True
        

        if card.cardtype == 'death':
            return gameover(team2, f"{team} team chose the death card")
        elif card.cardtype == team:
            team.current_score += 1
            if team.current_score >= team.winning_score:
                return gameover(team)
            else:
               return render_template("grid.html", cards=cards, cardtypes=cardtypes, message=message, team=team, blue=blue, red=red) 
        elif card.cardtype == team2:
            team2.current_score += 1
            if team2.current_score >= team2.winning_score:
                return gameover(team2)
            else:
                team = team2
                team2 = other_team(team)
                return render_template("grid.html", cards=cards, cardtypes=cardtypes, message=message, team=team, blue=blue, red=red)
        elif card.cardtype == 'blank':
            team = team2
            team2 = other_team(team)
            return render_template("grid.html", cards=cards, cardtypes=cardtypes, message=message, team=team, blue=blue, red=red)

        #return render_template("grid.html", cards=cards, cardtypes=cardtypes, message=message, team=team)
    else:
        return render_template("grid.html", cards=cards, cardtypes=cardtypes, message=message, team=team, blue=blue, red=red)

@app.route("/answers")
def answers():
    cardtypes = [str(card.cardtype).upper() for card in cards]
    return render_template("answers.html", cards=cards, cardtypes=cardtypes)
