import os

env = os.getenv('ENV')

if env == 'test':
    HOST = '192.168.0.108'
    PORT = 20000
    TOKEN = 'Schedule0350c8c75ddcd9fafdaA9738df4c9346bec48dc9c4915'


elif env == 'prod':
    HOST = '192.168.0.103'
    PORT = 9200
    TOKEN = 'Schedule0350c8c75ddcd9fafdaA9738df4c9346bec48dc9c4915'

else:
    HOST = '192.168.6.23'
    PORT = 9200
    TOKEN = 'Schedule0350c8c75ddcd9fafdaA9738df4c9346bec48dc9c4915'
    REDIS = '127.0.0.1'
    REDIS_PORT = 6379
    PUB_PORT = 14505
    MSG_CLIENT_PORT = 14506
    MSG_BACKEND_PORT = 14507
    HEART_PUB_PORT = 14508
    HEART_ROUTER_PORT = 14509
    SYNC_DIR = '/Users/admin/devops/schedule_sanic_zmq_server/sync_files'
