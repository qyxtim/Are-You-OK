import time
import db
import network
from login import require_login
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash

lastcheck = time.time()
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.secret_key = __name__
db_name = "websites.db"
format = "%Y-%m-%d %H:%M:%S"


@app.route('/')
def main():
    with db.open_db(db_name) as cursor:
        links = cursor.execute(
            "SELECT link, ts, state, description from urls").fetchall()
        response = []

        for link in links:
            d = {"link": link[0], "description": link[3]}
            if time.time() - time.mktime(time.strptime(str(link[1]), format)) > 60 or link[2] is None:
                re = network.ping(link[0])
                d["color"] = "green" if re is True else "red"
                cursor.execute("UPDATE urls SET state=?, ts=? where link=?", (re, time.strftime(
                    format, time.gmtime(time.time())), link[0]))
            else:
                d["color"] = "green" if re is True else "red"

            response.append(d)

    return render_template('index.html', subtitle="", response=response)


@app.route('/log', methods=['GET', 'POST'])
@require_login
def log():
    if request.method == 'POST':
        url = request.form.get('url')
        url = url if url.startswith('http') else ('https://' + url)
        desc = request.form.get('description')

        print(url, desc)

        if url is not None and desc is not None and url != "" and desc != "" and network.is_valid_url(url):
            with db.open_db(db_name) as cursor:
                cursor.execute(
                    "INSERT INTO urls (link, description) VALUES (?, ?)", (url, desc))

    return render_template("log.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', type=str)

        if username is not None and password is not None:
            with db.open_db(db_name) as cursor:
                ps = cursor.execute(
                    "SELECT password FROM users WHERE username = ?", (username, )).fetchall()
            if len(ps) == 1 and check_password_hash(ps[0][0], password):
                session["logged_in"] = True

    return render_template('login.html', status="logged_in" in session)


@app.route('/logout', methods=['POST'])
def logout():
    if "logged_in" in session:
        session.pop('logged_in')
    return redirect('/login')


if __name__ == '__main__':
    app.run()
