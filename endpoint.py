from sanic.response import json
from sanic import Blueprint
from sanic.exceptions import NotFound
from utils import auth


bp_db = Blueprint('db')


@bp_db.route('/es/query/', methods=['GET', 'POST'])
@auth('token')
async def query(req):
        app_name = req.json.get('app_name')
        keywords = req.json.get('keywords')
        daterange = req.json.get('daterange')
        # r = await es_query(app_name, keywords, daterange)
        return None


@bp_db.exception(NotFound)
def ignore_404s(request, exception):
    return json("404, {} not found ".format(request.url))