from sanic import Sanic
from endpoint import schedule

app = Sanic(__name__)
app.blueprint(schedule)



if __name__ == '__main__':
    app.run(host='0.0.0.0', workers=2, port=10011)
