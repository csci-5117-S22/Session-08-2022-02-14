from flask import Flask, render_template, request, g, redirect, url_for, jsonify

import db

app = Flask(__name__)

# have the DB submodule set itself up before we get started. groovy.
@app.before_first_request
def initialize():
    db.setup()

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/people', methods=['GET'])
def people():
    with db.get_db_cursor() as cur:
        cur.execute("SELECT * FROM person;")
        names = [record[1] for record in cur]

        return render_template("people.html", names=names)

@app.route('/people', methods=['POST'])
def new_person():
    name = request.form.get("name", "unknown name")
    app.logger.info("adding new friend %s", name)
    with db.get_db_cursor(commit=True) as cur:
        cur.execute("insert into person (name) values (%s);", (name,))    
    return redirect(url_for("people"))

@app.route("/api/whatev.json")
def api():
    data = {'daniel': 'low caff',
    'willow': {
        'type':'cat',
        'size': 7
    }}
    return jsonify(data)
