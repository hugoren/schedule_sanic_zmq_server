import uuid, time
from sanic.response import json
from sanic import Blueprint
from sanic.exceptions import NotFound
from utils import auth
from utils import retry_wait
from utils import redis_get
from service import sync


schedule = Blueprint('schedule')


@schedule.route('/api/v1/schedule/file_sync/', methods=['GET', 'POST'])
@auth('token')
async def file_sync(req):
        target = req.json.get('target')
        file_name = req.json.get('file_name')
        jid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(int(time.time() * 100000000000000000000000000000))))
        await sync(jid, target, file_name)

        @retry_wait(retry_count=90, interval_wait=2)
        def wait_result():
            r = redis_get(jid)
            if not r:
                raise Exception("还获取不到值，重试3分钟")
            return r
        return wait_result()


@schedule.exception(NotFound)
def ignore_404s(request, exception):
    return json("404, {} not found ".format(request.url))