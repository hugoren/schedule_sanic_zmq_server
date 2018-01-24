import uuid, time
from sanic.response import json
from sanic import Blueprint
from sanic.exceptions import NotFound
from sanic.exceptions import RequestTimeout
from utils import auth
from utils import retry_wait
from utils import Redis
from service import sync
from service import remote_command


schedule = Blueprint('schedule')


@schedule.route("/api/v1/schedule/file_sync/", methods=["GET", "POST"])
@auth("token")
async def file_sync(req):
    """
    指定同步目录
    单节点,单文件同步 node_id, file_name
    :param req:
    :return: dict
    """
    target = req.json.get("target")
    file_name = req.json.get("file_name")
    if isinstance(target, (str,)) and isinstance(file_name, (str,)):
        jid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(int(time.time() * 100000000000000000000000000000))))
        await sync(jid, target, file_name)
    else:
        return "传参格式不合格"

    @retry_wait(retry_count=9, interval_wait=1)
    def wait_result():
        r = Redis(1).get(jid)
        if not r:
            raise Exception("还获取不到任务，重试等待3分钟")
        return r
    return wait_result()


@schedule.route('/api/v1/schedule/command/', methods=['GET', 'POST'])
@auth('token')
async def commands(req):
    target = req.json.get("target")
    command = req.json.get("command", "command")
    script_name = req.json.get("script_name")
    fun_name = req.json.get('fun_name')
    args = req.json.get("args")
    kwargs = req.json.get("kwargs")
    jid = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(int(time.time() * 100000000000000000000000000000))))
    data = {"jid": jid, "target": target,
            "command": command, "script_name": script_name, "fun_name": fun_name,
            "args": args, "kwargs": kwargs
            }
    await remote_command(data)

    @retry_wait(retry_count=90, interval_wait=2)
    def wait_result():
        r = Redis(1).get(jid)
        if not r:
            raise Exception("retry")
        return r
    return wait_result()


@schedule.exception(NotFound)
def ignore_404s(request, exception):
    return json("404, {} not found, {1}".format(request.url, exception))


@schedule.exception(RequestTimeout)
def timeout(request, exception):
    return json('408, {0}'.format(exception))