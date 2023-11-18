from flask import Flask
from config import config_options

app = Flask(__name__)
app.config.from_object(config_options['development'])

from app import views
from app.auth import views
from app.account import views


