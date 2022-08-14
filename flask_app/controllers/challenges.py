from flask import render_template, session, redirect, request, flash
from crypt import methods
from flask_app import app
from flask_app.models.challenge import Challenge
from datetime import datetime

@app.route('/challenges')
def challenges():
    session.pop('challenge_id', None)
    return render_template('challenges.html', challenge = Challenge.get_all(), date = datetime.now())

@app.route('/new_challenge')
def new_challenge():
    return render_template('new_challenge.html')

@app.route('/create_challenge', methods=['POST'])
def create_challenge():
    challenge_id = Challenge.save_challenge(request.form)

    session['challenge_id'] = challenge_id

    return redirect('/challenges')

@app.route('/challenge/<int:id>')
def view(id):


    if 'participant_id' not in session:
        return redirect('/logout')
    return render_template('leaderboard.html', challenge = Challenge.get_all_by_id(id))

@app.route('/participate_in_challenge/<int:challenge_id>')
def participate(challenge_id):
    participant_id = session['participant_id']

    data = {
        'participants_id':participant_id,
        'challenges_id':challenge_id
    }

    if not Challenge.participate_validation(data):
        return redirect('/challenges')

    Challenge.p_in_c(data)

    return redirect('/challenges')

@app.route('/leaderboard/<int:challenge_id>')
def enter_leaderboard(challenge_id):

    if 'participant_id' not in session:
        return redirect('/logout')

    session['challenge_id'] = challenge_id

    return render_template('leaderboard.html', challenge = Challenge.get_leaderboard_table(challenge_id))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


