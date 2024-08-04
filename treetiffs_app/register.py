from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask_hashing import Hashing
import re
import os
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from treetiffs_app import app
from treetiffs_app import connect
from treetiffs_app.functions import getCursor
from treetiffs_app.functions import login_required
from treetiffs_app.functions import roles_required

hashing = Hashing(app)
PASSWORD_SALT = 'KsVUyGzItjo4kCg'

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    """This is the page with register form to let users register."""
    # Output message if something goes wrong...
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['birth_date']
        location = request.form['location']
        
        # Password validation
        if len(password) < 8 or not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
            msg = 'Password must be at least 8 characters long and contain both letters and digits.'
            return render_template('register.html', msg=msg, username=username, email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, location=location)

        cursor = getCursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # If account exists show error and validation checks
        if user:
            msg = 'Username already exists!'
            return render_template('register.html', msg=msg, username=username, email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, location=location)
        
        # If everything is OK, register the user
        password_hash = hashing.hash_value(password, salt=PASSWORD_SALT)
        cursor.execute('''INSERT INTO users (username, email, password_hash, first_name, last_name, birth_date, location, role, status, profile_image)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (username, email, password_hash, first_name, last_name, date_of_birth, location, 'member', 'active', 'default.png'))
        msg = 'Registration successful!'
        return redirect(url_for('login', msg=msg))
    return render_template('register.html', msg=msg)
