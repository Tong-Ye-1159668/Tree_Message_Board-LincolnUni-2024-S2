from flask import Flask

app = Flask(__name__)
app.secret_key = 'KEXq3sLJCV'
UPLOAD_FOLDER = 'static/profile_images'
app.config['UPLOAD_FOLDER'] = 'static/profile_images'

from treetiffs_app import login
from treetiffs_app import register
from treetiffs_app import messages
from treetiffs_app import profiles
from treetiffs_app import user_management