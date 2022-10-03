
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from dash4 import app1
from flask import Flask

#unused base app
base_app = Flask(__name__)

app = DispatcherMiddleware(base_app, {
    '/app1': app1.server
})
