from flask import Flask, request
from flask_restful import Api
from delivery import get_best_routes, Location

app = Flask(__name__)
api = Api(app)

MOCK_AGENT_URL = 'http://mockbcknd.tk/'


@app.route('/get_routes')
def get_routes():
    pickup_coords = request.args['pickup_point'].split(',')
    dest_coords = request.args['dest_point'].split(',')

    pickup_point = Location(pickup_coords[0], pickup_coords[1])
    dest_point = Location(dest_coords[0], dest_coords[1])

    return str(get_best_routes(pickup_point, dest_point))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')
