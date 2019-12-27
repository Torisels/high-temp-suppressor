from flask import Flask
import threading
app = Flask(__name__)
from web_app import routes

