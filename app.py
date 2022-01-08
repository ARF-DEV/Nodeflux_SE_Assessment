import requests
from flask import Flask
from flask import request

from routes.index import index_route
from routes.yearly import yearly_route
from routes.monthly import monthly_route
from routes.daily import daily_route
from routes.utils.utils import *

app = Flask(__name__)
app.register_blueprint(index_route, url_prefix="/")
app.register_blueprint(yearly_route, url_prefix="/yearly")
app.register_blueprint(monthly_route, url_prefix="/monthly")
app.register_blueprint(daily_route, url_prefix="/daily")

