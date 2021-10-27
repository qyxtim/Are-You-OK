""" This file is only used for creating a new database if the database doesn't exist. """

import db
import os
from werkzeug.security import generate_password_hash

db_name = "websites.db"

if not os.path.exists(db_name):
    open(db_name, 'w').close()
    with db.open_db(db_name) as cursor:
        cursor.execute(
            "create table urls(id INTEGER PRIMARY KEY, ts timestamp default current_timestamp, state BOOLEAN, link TEXT NOT NULL, description TEXT NOT NULL);")
        username = input("Please input admin's username:")
        password = input("Please input admin's password:")
        cursor.execute(
            "create table users(username TEXT NOT NULL, password TEXT NOT NULL);")
        cursor.execute("Insert into users (username, password) values (?, ?)",
                       (username, generate_password_hash(password)))
