from flask_smorest import Blueprint

bp = Blueprint('post', __name__, description="desciption of posts", url_prefix='/post' )

from . import routes