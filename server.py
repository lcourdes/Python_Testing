import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def addAlreadyBoughtPlaces(competitions):
    for competition in competitions:
        competition['alreadyBoughtPlaces'] = {}
    return competitions


def backUpBoughtPlaces(competition, club, boughtPlaces):
    if competition['alreadyBoughtPlaces'].get(club['email']):
        competition['alreadyBoughtPlaces'][club['email']] = (
            int(competition['alreadyBoughtPlaces'][club['email']])
            + int(boughtPlaces)
            )
        return competition
    competition['alreadyBoughtPlaces'][club['email']] = int(boughtPlaces)
    return competition


loadedCompetitions = loadCompetitions()
competitions = addAlreadyBoughtPlaces(loadedCompetitions)
clubs = loadClubs()


def create_app(config={}):
    app = Flask(__name__)
    app.config.from_object(config)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        try:
            emailInput = request.form['email']
            club = [club for club in clubs if club['email'] == emailInput][0]
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)
        except IndexError:
            flash("Sorry, that email wasn't found.")
            return render_template('index.html')

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in clubs if c['name'] == club]
        foundCompetition = [c for c in competitions
                            if c['name'] == competition]
        if not foundClub:
            flash("Something went wrong-please login")
            return render_template('index.html')
        if not foundCompetition:
            flash("Something went wrong-please try again")
            return render_template('welcome.html',
                                   club=foundClub[0],
                                   competitions=competitions)

        datetime_object = datetime.strptime(foundCompetition[0]['date'],
                                            '%Y-%m-%d %H:%M:%S')
        if datetime.now() > datetime_object:
            flash("This is a past event. Please choose a future competition.")
            return render_template('welcome.html',
                                   club=foundClub[0],
                                   competitions=competitions)
        return render_template('booking.html',
                               club=foundClub[0],
                               competition=foundCompetition[0])

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        inputName = request.form['competition']
        competition = [c for c in competitions if c['name'] == inputName][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        if placesRequired > int(club['points']):
            flash('You do not have enough points. Try again')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)
        if placesRequired > 12:
            flash('You can\'t purchase more than 12 places.')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)
        if competition['alreadyBoughtPlaces'].get(club['email']):
            alreadyBoughtPlaces = competition['alreadyBoughtPlaces'].get\
                (club['email'])
            if placesRequired + int(alreadyBoughtPlaces) > 12:
                flash(f'You can\'t purchase more than 12 places and you have \
                      already bought {alreadyBoughtPlaces}')
                return render_template('booking.html',
                                       club=club,
                                       competition=competition)
        if placesRequired > int(competition['numberOfPlaces']):
            flash('You can\'t purchase more than available places.')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)
        competition['numberOfPlaces'] = (int(competition['numberOfPlaces']) -
                                         placesRequired)
        competition = backUpBoughtPlaces(competition, club, placesRequired)
        club['points'] = int(club['points']) - placesRequired
        flash(f'Great-booking complete! You just bought {placesRequired} \
              places.')
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)

    @app.route('/clubs')
    def displayClubs():
        return render_template('clubs.html', clubs=clubs)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app
