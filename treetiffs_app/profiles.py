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

# Define the upload folder for profile images
UPLOAD_FOLDER = 'static/profile_images'
app.config['UPLOAD_FOLDER'] = 'treetiffs_app/static/profile_images'

# Create the upload folder if it does not exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

db_connection = None

# Profile page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
@active_required
def profile():
    """This is the profile page of the user."""
    cursor = getCursor()
    if request.method == 'POST':
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birth_date = request.form['birth_date']
        location = request.form['location']

        # Update the user's profile details
        cursor.execute('''UPDATE users SET email=%s, first_name=%s, last_name=%s, birth_date=%s, location=%s WHERE user_id=%s''',
                       (email, first_name, last_name, birth_date, location, session['user_id']))
        flash('Profile details successfully updated.', 'success')
        return redirect(url_for('profile'))
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()
    return render_template('profile.html', user=user)

# Route for updating the profile image
@app.route('/profile/image', methods=['POST'])
@login_required
@active_required
def update_profile_image():
    """This route is for updating the profile image."""
    # Check if the POST request has the file part
    if 'profile_image' not in request.files:
        return redirect(url_for('profile'))
    
    # Get the image file from the POST request
    file = request.files['profile_image']
    if file.filename == '':
        return redirect(url_for('profile'))
    
    # Rename the file to make sure it must be unique from other users' profile images
    timestamp = datetime.now().strftime('%d%m%Y_%H%M%S')
    extension = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{timestamp}_{session['username']}.{extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    cursor = getCursor()
    # Update the user's profile image
    cursor.execute("UPDATE users SET profile_image = %s WHERE user_id = %s", (filename, session['user_id']))

    session['profile_image'] = filename
    flash('Profile image successfully updated.', 'success')
    return redirect(url_for('profile'))

# Route for removing the profile image to the default image
@app.route('/profile/image/remove', methods=['POST'])
@login_required
@active_required
def remove_profile_image():
    """This route is for removing the profile image."""
    default_image = 'default.png'
    cursor = getCursor()
    cursor.execute("SELECT profile_image FROM users WHERE user_id = %s", (session['user_id'],))
    current_image = cursor.fetchone()['profile_image']

    # Change the user's profile image back to the default image
    cursor.execute("UPDATE users SET profile_image = %s WHERE user_id = %s", (default_image, session['user_id']))
    
    if current_image != default_image:
        old_image_path = os.path.join(app.config['UPLOAD_FOLDER'], current_image)
        if os.path.exists(old_image_path):
            os.remove(old_image_path)
    
    session['profile_image'] = default_image
    flash('Profile image successfully removed.', 'success')
    return redirect(url_for('profile'))

# Route for changing the user's password
@app.route('/profile/password', methods=['POST'])
@login_required
@active_required
def change_password():
    """This route is for changing the user's password."""

    # Get the form data
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    
    cursor = getCursor()
    cursor.execute("SELECT password_hash FROM users WHERE user_id = %s", (session['user_id'],))
    user = cursor.fetchone()
    
    # Check if the current password is correct
    if not hashing.check_value(user['password_hash'], current_password, salt=PASSWORD_SALT):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('profile'))
    
    # Check if the new password and confirm password match
    if new_password != confirm_password:
        flash('The passwords do not match.', 'danger')
        return redirect(url_for('profile'))
    
    # Check if the new password is different from the current password
    if hashing.check_value(user['password_hash'], new_password, salt=PASSWORD_SALT):
        flash('New password must be different from the current password.', 'danger')
        return redirect(url_for('profile'))
    
    # Check if the new password meets the requirements
    if len(new_password) < 8 or not re.search(r'\d', new_password) or not re.search(r'[a-zA-Z]', new_password):
        flash('Password must be at least 8 characters long and include both letters and numbers.', 'danger')
        return redirect(url_for('profile'))
    
    # Update the user's password
    new_password_hash = hashing.hash_value(new_password, salt=PASSWORD_SALT)
    cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (new_password_hash, session['user_id']))
    
    flash('Password successfully updated.', 'success')
    return redirect(url_for('profile'))
