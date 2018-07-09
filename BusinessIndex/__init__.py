from flask import Flask
from BusinessIndex.appconfig import Config

app = Flask(__name__)

app.config.from_object(Config)


from BusinessIndex import routes
