from app import app
from flask import render_template, request
from flask_frozen import Freezer
import sys
import os, smtplib
freezer = Freezer(app)
from guessRaga import *
def validate(phrase):
    if len(phrase) == 0:
        guesses =  'Your phrase is empty.'
    for note in phrase:
        if note not in 'SrRgGMmPdDnN- ':
            guesses =  'Your phrase has a letter which is not a note. Please reenter your phrase.'
    while '-' in phrase:
       phrase = phrase.replace('-', '')
    if len(phrase) < 5:
        guesses = 'Your phrase is too short. Please enter a longer phrase.'
    else:
        guesses = getRagas(phrase)
    
    if not guesses:
        guesses = 'I\'m not sure what raga your phrase is in.'
    elif guesses[0:2] == 'Yo':
        pass
    else:
        guesses = 'I think your phrase is in Raga ' + guesses
    return guesses
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/', methods=['GET', 'POST'])
def guess():
    phrase = request.form['phrase']
    guesses = validate(phrase)
    return render_template('index.html', guesses=guesses)
@app.route('/findex')
def fdindex():
    return render_template('feedback.html')

@app.route('/feedback', methods=['POST'])
def fdbk():
    pw = os.getenv('PASS')
    con = smtplib.SMTP('smtp.gmail.com', 587)
    name = request.form['name']
    fdbk = request.form['fdbk']
    if not fdbk:
        print('no feedback')
        fs = 'There is no feedback. Please enter some feedback and try again.'
        return render_template('feedback.html', fds=fs)
    if name:
        et = fdbk + '\n\nSincerely, \n ' + name
    else:
        et = fdbk + '\n\nSincerely,\nA User'

    con.starttls()
    con.login('findprajju@gmail.com', pw)
    con.sendmail('findprajju@gmail.com', 'findprajju@gmail.com', 'Subject: Guess Raga Feedback\n\n' + et)
    con.quit()
    fs = 'Feedback sent successfully.'
    return render_template('feedback.html', fds=fs)
@app.route('/dcindex')
def dci():
    return render_template('datacollection.html', fds='')

@app.route('/datacollection', methods=['POST'])
def dc():
    out = 'Data recorded. Thanks for your time!'
    phrase = list(request.form['phrase'])
    raga = request.form['raga']
    f= open('data.csv')
    if ''.join(phrase) in str(f.read()):
        out = 'This phrase has already been recorded.'
        return render_template('datacollection.html', fds=out)
    while '-' in phrase:
        del phrase[phrase.index('-')]
    if len(phrase) < 5:
        out = 'Your phrase is too short. Please try again.'
        return render_template('datacollection.html', fds=out)
    for w in phrase:
        if w not in 'SRGMPDNrgmdn- ':
            out = 'Your phrase contains a letter which is not a note. Please try again.'    
            return render_template('datacollection.html', fds=out)
    if not raga:
        out = 'Oops! You haven\'t filled out the Raga field yet.'
        return render_template('datacollection.html', fds=out)

    f = open('data.csv', 'a')
    f.write('\n' + ', '.join([''.join(phrase), raga]))
    f.close()
    return render_template('datacollection.html', fds=out)
    