import time
import db
import network
from login import require_login
from flask import Flask, render_template, request, session, redirect
from werkzeug.security import check_password_hash

app = Flask(__name__)

# Set session
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
app.secret_key = __name__

# db_name
db_name = "websites.db"

# format time created by sqlite
format = "%Y-%m-%d %H:%M:%S"

# Update Frequency. Default: 60 seconds
frequency = 60


@app.route('/')
def main():
    """ Render index page and retrieve data from database """
    response = []

    try:
        with db.open_db(db_name) as cursor:
            links = cursor.execute(
                "SELECT link, ts, state, description from urls").fetchall()
            for link in links:
                d = {"link": link[0], "description": link[3]}
                if time.time() - time.mktime(time.strptime(str(link[1]), format)) > frequency or link[2] is None:
                    re = network.ping(link[0])
                    d["color"] = "green" if re is True else "red"
                    cursor.execute("UPDATE urls SET state=?, ts=? where link=?", (re, time.strftime(
                        format, time.gmtime(time.time())), link[0]))
                else:
                    d["color"] = "green" if re is True else "red"

                response.append(d)
    except Exception as e:
        print("Error: " + str(e))

    return render_template('index.html', response=response, status="logged_in" in session)


@app.route('/log', methods=['GET', 'POST'])
@require_login
def log():
    """ Render log website page """
    if request.method == 'POST':
        url = request.form.get('url')
        url = url if url.startswith('http') else ('https://' + url)
        desc = request.form.get('description')

        if url is not None and desc is not None and url != "" and desc != "" and network.is_valid_url(url):
            try:
                with db.open_db(db_name) as cursor:
                    cursor.execute(
                        "INSERT INTO urls (link, description) VALUES (?, ?)", (url, desc))
            except Exception as e:
                print("Error: " + str(e))

    return render_template("log.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Support the login function of the website """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', type=str)

        if username is not None and password is not None:
            try:
                with db.open_db(db_name) as cursor:
                    ps = cursor.execute(
                        "SELECT password FROM users WHERE username = ?", (username, )).fetchall()
                if len(ps) == 1 and check_password_hash(ps[0][0], password):
                    session["logged_in"] = True
            except Exception as e:
                print("Error: ", str(e))

    return render_template('login.html', status="logged_in" in session)


@app.route('/logout', methods=['POST'])
def logout():
    """ Enable user to log out """
    if "logged_in" in session:
        session.pop('logged_in')
    return redirect('/login')


@app.route('/delete', methods=['POST'])
@require_login
def delete():
    """ Enable user to delete the website logged in before """
    link = request.form.get('link')

    if link is not None and network.is_valid_url(link):
        try:
            with db.open_db(db_name) as cursor:
                cursor.execute("Delete from urls where link = ?", (link,))
        except Exception as e:
            print("Error: ", str(e))

    return redirect('/')


if __name__ == '__main__':
    app.run()
