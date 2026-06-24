from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
users = {
    'admin': '12345'

}
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

class SurveyResult(db.Model):
    __tablename__ = "survey_results"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(100))
    favorite_animal = db.Column(db.String(100))
    favorite_games = db.Column(db.Text)
    favorite_food = db.Column(db.String(100))
    favorite_gadget = db.Column(db.String(100))
    favorite_roblox_game = db.Column(db.Text)
    source = db.Column(db.String(100))

with app.app_context():
    db.create_all()



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    number = request.form.get('number')
    if not number:
        return render_template('home.html', error='Please enter a number')
    return redirect(url_for('survey', number=number))
@app.route('/survey', methods=['GET', 'POST'])
def survey():
    number = request.args.get('number')
    if request.method == 'POST':
        favorite_animal = request.form.get('favorite_animal')
        favorite_games = request.form.getlist('favorite games')
        favorite_food = request.form.get('favorite food')
        favorite_gadget = request.form.get('favorite gadget')
        favorite_roblox_game = request.form.getlist('favorite roblox game')
        source = request.form.get('source')

        favorite_games_str = ','.join(favorite_games)
        favorite_roblox_game_str = ','.join(favorite_roblox_game)

        result = SurveyResult(
            number=number,
            favorite_animal=favorite_animal,
            favorite_games=favorite_games_str,
            favorite_food=favorite_food,
            favorite_gadget=favorite_gadget,
            favorite_roblox_game = favorite_roblox_game_str,
            source = source
        )

        db.session.add(result)
        db.session.commit()

        return render_template('ThankYou.html')
    return render_template('survey.html', number=number)

@app.route('/results')
@auth.login_required
def results():
    date = SurveyResult.query.all()
    return render_template('results.html', data=date)

if __name__ == '__main__':
    app.run(debug=True, port = 5001)