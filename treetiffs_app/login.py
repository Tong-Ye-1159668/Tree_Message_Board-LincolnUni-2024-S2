from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import flash
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
from treetiffs_app.functions import active_required

hashing = Hashing(app)
PASSWORD_SALT = 'KsVUyGzItjo4kCg'

UPLOAD_FOLDER = 'static/profile_images'
app.config['UPLOAD_FOLDER'] = 'static/profile_images'

db_connection = None


# Login page
@app.route('/')
@active_required
def index():
    """This is the home page of the application.  
    It is also the page that users are redirected to after they log in."""
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        
        # Fetch one record and return result
        account = cursor.fetchone()

        if account is not None:
            password_hash = account['password_hash']
            if hashing.check_value(password_hash, user_password, PASSWORD_SALT):
            # If account exists in accounts table 
                if account['status'] == 'inactive':
                    msg = 'Your account is inactive. Please contact the administrator.'
                    return render_template('login.html', msg=msg)
                else:    
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']
                    return redirect(url_for('index'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'

    # Show the login form with message (if any)
    flash('You have successfully logged in', 'success')
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('user_id', None)
   session.pop('username', None)

   # Redirect to login page
   return redirect(url_for('index'))

# Disply an error message if the user is inactive
@app.route('/inactive_account')
def inactive_account():
    return render_template('inactive_account.html')


if __name__ == '__main__':
    app.run(debug=True)
