from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_httpauth import HTTPBasicAuth
app = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    'admin': '12345'

}
@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS survey_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        number INTEGER,
        favorite_animal TEXT,
        favorite_games TEXT,
        favorite_food TEXT,
        favorite_gadget TEXT,
        favorite_roblox_game TEXT,
        source TEXT
    )
    ''')
    conn.commit()
    conn.close()
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


        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO survey_results
         
         (number, favorite_animal, favorite_games, favorite_food, favorite_gadget, favorite_roblox_game, source)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ''',(number, favorite_animal, favorite_games_str,  favorite_food, favorite_gadget, favorite_roblox_game_str, source))

        conn.commit()
        conn.close()
        return render_template('ThankYou.html')
    return render_template('survey.html', number=number)

@app.route('/results')
@auth.login_required
def results():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT*FROM survey_results''')
    data = cursor.fetchall()
    conn.close()
    return render_template('results.html', data=data)

init_db()
if __name__ == '__main__':
    app.run(debug=True, port = 5001)