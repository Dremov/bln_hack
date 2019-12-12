from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from delivery import get_best_routes
from api_processing_lambda import get_agents

import requests
import json

app = Flask(__name__)
api = Api(app)

MOCK_AGENT_URL = 'http://mockbcknd.tk/'


@app.route('/get_routes')
def get_routes():
    pickup_point = request.args['pickup_point']
    dest_point = request.args['dest_point']

    # print(get_routes())
    # print('yo')

    return str(json.loads(get_best_routes()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5002')
