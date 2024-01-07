from flask import Flask

app = Flask(__name__)

from resources.post import routes
from resources.user import routes
